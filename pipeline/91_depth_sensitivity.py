"""Does the HEALPix depth change the water surface? Akgöl and Meyil, every scene valid at depth 17.

For each scene the same Landsat pixels (green, NIR, QA_PIXEL as in 01_landsat_scenes.py) give three areas:
  * depth 17 (~50 m cells, 0.25 ha), the method of the replication;
  * depth 18 (~25 m cells, 0.06 ha), the first HEALPix level finer than the 30 m pixel;
  * native pixels: NDWI > 0 on the 30 m pixels whose centre lies in the site outline, area 900 m2 each
    (UTM; scale error < 0.1 %), no grid at all, as the paper measured it.
Same masking, same NDWI threshold (> 0), and the 95 % valid rule applied at each depth.
Akgöl is the headline claim; Meyil (a few ha) is the smallest site, where a coarse cell matters most.

Usage: python pipeline/91_depth_sensitivity.py <ROOT>
Reads <ROOT>/landsat/scenes.csv and <ROOT>/aoi/; writes <ROOT>/landsat/depth_sensitivity.csv (resumable) and
results/depth_sensitivity.json.
"""
import csv
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd
import planetary_computer
import pystac_client
import rasterio
import shapely
from pyproj import Transformer
from shapely.geometry import shape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

ROOT = sys.argv[1]
SITES = ["akgol", "meyil"]
OUT = f"{ROOT}/landsat/depth_sensitivity.csv"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
BAD_BITS = (1 << 0) | (1 << 1) | (1 << 3) | (1 << 4) | (1 << 5)
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY="5", GDAL_HTTP_RETRY_DELAY="10",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
FIELDS = ["site", "scene", "datetime", "ha_d17", "ha_d18", "ha_native", "valid_d17", "valid_d18", "valid_native"]
lock = threading.Lock()


def outline(key):
    g = shape(json.load(open(f"{ROOT}/aoi/{key}.geojson"))["geometry"])
    ring = np.asarray(g.exterior.coords) if g.geom_type == "Polygon" else np.asarray(
        max(g.geoms, key=lambda p: p.area).exterior.coords)
    return g, ring[:-1]


def read_band(href, bounds_ll):
    x0, y0, x1, y1 = bounds_ll
    with rasterio.Env(**ENV), rasterio.open(href) as r:
        tr = Transformer.from_crs(4326, r.crs, always_xy=True)
        xs, ys = tr.transform([x0, x1, x0, x1], [y0, y0, y1, y1])
        w = rasterio.windows.from_bounds(min(xs) - 60, min(ys) - 60, max(xs) + 60, max(ys) + 60,
                                         r.transform).round_offsets().round_lengths()
        return r.read(1, window=w, boundless=True, fill_value=0), r.window_transform(w), r.crs


def process(item, key, site):
    hrefs = {k: planetary_computer.sign(item.assets[k].href) for k in ("green", "nir08", "qa_pixel")}
    b = site["geom"].bounds
    g, tr, crs = read_band(hrefs["green"], b)
    n, _, _ = read_band(hrefs["nir08"], b)
    q, _, _ = read_band(hrefs["qa_pixel"], b)
    bad = (q == 0) | ((q & BAD_BITS) != 0) | (g == 0) | (n == 0)
    gr = np.where(bad, np.nan, g * 0.0000275 - 0.2).ravel()
    nr = np.where(bad, np.nan, n * 0.0000275 - 0.2).ravel()
    rows, cols = np.mgrid[0:g.shape[0], 0:g.shape[1]]
    x, y = rasterio.transform.xy(tr, rows.ravel(), cols.ravel())
    lon, lat = Transformer.from_crs(crs, 4326, always_xy=True).transform(np.asarray(x), np.asarray(y))
    row = {"site": key, "scene": item.id, "datetime": item.properties["datetime"]}
    for d in (17, 18):
        op = common.BilinearToCells(lon, lat, site[f"cells{d}"], depth=d)
        gc, valid = op(gr)
        nc, _ = op(nr)
        vshare = float(np.nanmean(np.where(np.isfinite(valid), valid, 0) >= 0.5))
        with np.errstate(invalid="ignore", divide="ignore"):
            ndwi = (gc - nc) / (gc + nc)
        row[f"valid_d{d}"] = round(vshare, 4)
        row[f"ha_d{d}"] = round(float((ndwi > 0).sum() * common.cell_area_ha(d)), 2)
    inside = shapely.contains_xy(site["geom"], lon, lat)
    ok = inside & np.isfinite(gr) & np.isfinite(nr)
    with np.errstate(invalid="ignore", divide="ignore"):
        ndwi_px = (gr - nr) / (gr + nr)
    row["valid_native"] = round(float(ok.sum() / max(inside.sum(), 1)), 4)
    row["ha_native"] = round(float((ok & (ndwi_px > 0)).sum() * 900 / 1e4), 2)
    return row


def summarise():
    df = pd.read_csv(OUT)
    ok = (df.valid_d17 >= 0.95) & (df.valid_d18 >= 0.95) & (df.valid_native >= 0.95)
    df = df[ok].copy()
    df["year"] = pd.to_datetime(df.datetime).dt.year
    out = {"scenes_valid_at_all_three": {}, "sites": {}}
    for key, g in df.groupby("site"):
        big = g[g.ha_native >= 1]                        # relative differences only where there is water
        s = {"scenes": int(len(g)), "scenes_with_at_least_1_ha_water": int(len(big)),
             "median_ha": {c: round(float(g[c].median()), 1) for c in ("ha_d17", "ha_d18", "ha_native")},
             "max_ha": {c: round(float(g[c].max()), 1) for c in ("ha_d17", "ha_d18", "ha_native")}}
        for c in ("ha_d17", "ha_d18"):
            rel = 100 * (big[c] - big.ha_native) / big.ha_native
            s[f"{c}_vs_native_pct"] = {"median": round(float(rel.median()), 1), "p05": round(float(rel.quantile(.05)), 1),
                                       "p95": round(float(rel.quantile(.95)), 1)}
            s[f"{c}_vs_native_abs_ha"] = {"median": round(float((g[c] - g.ha_native).abs().median()), 2),
                                          "max": round(float((g[c] - g.ha_native).abs().max()), 2)}
        rel18 = 100 * (big.ha_d18 - big.ha_d17) / big.ha_d17.where(big.ha_d17 > 0)
        s["d18_vs_d17_pct"] = {"median": round(float(rel18.median()), 1), "p05": round(float(rel18.quantile(.05)), 1),
                               "p95": round(float(rel18.quantile(.95)), 1)}
        if key == "akgol":                                   # the paper's four years: scene closest to its value
            paper = {1987: 2958.4, 1998: 1153.9, 2007: 12.7, 2017: 117.2}
            yrs = {}
            for y, pv in paper.items():
                gy = g[g.year == y]
                if len(gy):
                    i = (gy.ha_d17 - pv).abs().idxmin()
                    yrs[str(y)] = {"paper_ha": pv, "scene": gy.loc[i, "scene"],
                                   **{c: float(gy.loc[i, c]) for c in ("ha_d17", "ha_d18", "ha_native")}}
            s["paper_years_closest_scene_at_d17"] = yrs
        out["sites"][key] = s
    json.dump(out, open("results/depth_sensitivity.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


def main():
    os.makedirs("results", exist_ok=True)
    sc = pd.read_csv(f"{ROOT}/landsat/scenes.csv")
    sc = sc[sc.site.isin(SITES) & sc["water_ha_ndwi_+0.0"].notna()]
    done = set()
    if os.path.exists(OUT):
        done = set(map(tuple, pd.read_csv(OUT)[["site", "scene"]].values))
    else:
        with open(OUT, "w", newline="") as f:
            csv.DictWriter(f, FIELDS).writeheader()
    sites = {}
    for k in SITES:
        geom, ring = outline(k)
        sites[k] = {"geom": geom, "cells17": common.polygon_cells(ring, depth=17),
                    "cells18": common.polygon_cells(ring, depth=18)}
        print(k, len(sites[k]["cells17"]), "cells at depth 17,", len(sites[k]["cells18"]), "at depth 18", flush=True)
    todo = [(r.site, r.scene) for r in sc.itertuples() if (r.site, r.scene) not in done]
    print(len(todo), "scene-site pairs to process", flush=True)
    cat = pystac_client.Client.open(STAC)
    ids = sorted({s for _, s in todo})
    items = {}
    for i in range(0, len(ids), 100):
        for it in cat.search(collections=["landsat-c2-l2"], ids=ids[i:i + 100]).items():
            items[it.id] = it
    n = 0
    with ThreadPoolExecutor(8) as ex:
        futs = {ex.submit(process, items[s], k, sites[k]): (k, s) for k, s in todo if s in items}
        for fu in as_completed(futs):
            try:
                row = fu.result()
            except Exception as e:
                print("FAIL", futs[fu], type(e).__name__, str(e)[:150], flush=True)
                continue
            with lock, open(OUT, "a", newline="") as f:
                csv.DictWriter(f, FIELDS).writerow(row)
            n += 1
            if n % 100 == 0:
                print(n, "done", flush=True)
    summarise()


if __name__ == "__main__":
    main()

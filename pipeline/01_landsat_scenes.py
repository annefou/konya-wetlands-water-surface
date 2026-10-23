"""Water surface of each site in every Landsat scene, 1984-2025, on HEALPix cells.

Source: Landsat Collection 2 Level-2 surface reflectance (USGS), served by Microsoft Planetary Computer
(collection "landsat-c2-l2", anonymous signed URLs, no account); Landsat 5 TM, 7 ETM+, 8 OLI, 9 OLI-2.
Per scene and site:
  1. read green, NIR and QA_PIXEL for the site window (COG, windowed HTTP read), scale to reflectance
     (DN x 0.0000275 - 0.2), mask fill, dilated cloud, cloud, cloud shadow and snow (QA bits 0, 1, 3, 4, 5);
  2. resample green and NIR onto the site's HEALPix cells (depth 17, ~49 m, healpix-geo WGS84) with
     healpix-resample, conservative bilinear, BEFORE any index or threshold (masked pixels excluded);
  3. NDWI = (green - NIR) / (green + NIR) per cell, as in Musaoglu et al. 2018 (McFeeters 1996); water where
     NDWI > 0 (the paper's "positive values"), with -0.1 and +0.1 as sensitivity thresholds;
  4. keep the scene for the site when at least 95 % of its cells are valid; water area = water cells x cell area.
Landsat 7 after 31 May 2003 has scan-line gaps, so most of its scenes fail the 95 % rule (reported).

Usage: python pipeline/01_landsat_scenes.py <ROOT> [<Y0> <Y1>]
Appends to <ROOT>/landsat/scenes.csv (one row per scene and site, resumable).
"""
import csv
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pystac_client
import planetary_computer
import rasterio
from rasterio.windows import from_bounds
from pyproj import Transformer
import shapely
from shapely.geometry import shape, box

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

ROOT = sys.argv[1]
Y0, Y1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1984, 2025)
OUT = f"{ROOT}/landsat/scenes.csv"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
THRESHOLDS = (-0.1, 0.0, 0.1)
MIN_VALID = 0.95
BAD_BITS = (1 << 0) | (1 << 1) | (1 << 3) | (1 << 4) | (1 << 5)
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY="5", GDAL_HTTP_RETRY_DELAY="10",
           CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif")
FIELDS = ["site", "scene", "platform", "datetime", "valid_share", "n_cells"] + [f"water_ha_ndwi_{t:+.1f}" for t in THRESHOLDS]
lock = threading.Lock()


def load_sites():
    import json
    sites = {}
    for k in common.SITES:
        g = shape(json.load(open(f"{ROOT}/aoi/{k}.geojson"))["geometry"])
        cells = np.load(f"{ROOT}/aoi/{k}_cells.npy")
        sites[k] = {"geom": g, "cells": cells}
    return sites


def read_band(href, bounds_ll):
    """Window of one band around the site, in the file's own CRS (read from the file itself)."""
    x0, y0, x1, y1 = bounds_ll
    with rasterio.Env(**ENV), rasterio.open(href) as r:
        tr = Transformer.from_crs(4326, r.crs, always_xy=True)
        xs, ys = tr.transform([x0, x1, x0, x1], [y0, y0, y1, y1])
        w = from_bounds(min(xs) - 60, min(ys) - 60, max(xs) + 60, max(ys) + 60, r.transform).round_offsets().round_lengths()
        a = r.read(1, window=w, boundless=True, fill_value=0)
        return a, r.window_transform(w), r.crs


def process(item, key, site):
    hrefs = {k: planetary_computer.sign(item.assets[k].href) for k in ("green", "nir08", "qa_pixel")}
    b = site["geom"].bounds
    g, tr, crs = read_band(hrefs["green"], b)
    n, _, _ = read_band(hrefs["nir08"], b)
    q, _, _ = read_band(hrefs["qa_pixel"], b)
    bad = (q == 0) | ((q & BAD_BITS) != 0) | (g == 0) | (n == 0)
    gr = np.where(bad, np.nan, g * 0.0000275 - 0.2)
    nr = np.where(bad, np.nan, n * 0.0000275 - 0.2)
    rows, cols = np.mgrid[0:g.shape[0], 0:g.shape[1]]
    x, y = rasterio.transform.xy(tr, rows.ravel(), cols.ravel())
    lon, lat = Transformer.from_crs(crs, 4326, always_xy=True).transform(np.asarray(x), np.asarray(y))
    op = common.BilinearToCells(lon, lat, site["cells"])
    gc, valid = op(gr.ravel())
    nc, _ = op(nr.ravel())
    vshare = float(np.nanmean(np.where(np.isfinite(valid), valid, 0) >= 0.5))
    row = {"site": key, "scene": item.id, "platform": item.properties.get("platform"),
           "datetime": item.properties["datetime"], "valid_share": round(vshare, 4), "n_cells": len(site["cells"])}
    with np.errstate(invalid="ignore", divide="ignore"):
        ndwi = (gc - nc) / (gc + nc)
    for t in THRESHOLDS:
        row[f"water_ha_ndwi_{t:+.1f}"] = round(float((ndwi > t).sum() * common.cell_area_ha()), 2) if vshare >= MIN_VALID else ""
    return row


def main():
    os.makedirs(f"{ROOT}/landsat", exist_ok=True)
    sites = load_sites()
    done = set()
    if os.path.exists(OUT):
        with open(OUT) as f:
            done = {(r["site"], r["scene"]) for r in csv.DictReader(f)}
    else:
        with open(OUT, "w", newline="") as f:
            csv.DictWriter(f, FIELDS).writeheader()
    allb = shapely.unary_union([s["geom"] for s in sites.values()]).bounds
    cat = pystac_client.Client.open(STAC)
    for year in range(Y0, Y1 + 1):
        t0 = time.time()
        items = list(cat.search(collections=["landsat-c2-l2"], bbox=allb, datetime=f"{year}-01-01/{year}-12-31",
                                query={"eo:cloud_cover": {"lt": 70}}).items())
        jobs = []
        for it in items:
            foot = shape(it.geometry)
            for k, s in sites.items():
                if foot.contains(box(*s["geom"].bounds)) and (k, it.id) not in done:
                    jobs.append((it, k, s))
        n_ok = 0
        with ThreadPoolExecutor(8) as ex:
            futs = {ex.submit(process, it, k, s): (it.id, k) for it, k, s in jobs}
            for fu in as_completed(futs):
                try:
                    row = fu.result()
                except Exception as e:
                    print("FAIL", futs[fu], type(e).__name__, str(e)[:150], flush=True)
                    continue
                n_ok += 1
                with lock, open(OUT, "a", newline="") as f:
                    csv.DictWriter(f, FIELDS).writerow(row)
        print(f"{year}: {len(items)} scenes, {len(jobs)} scene-site jobs, {n_ok} done, {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()

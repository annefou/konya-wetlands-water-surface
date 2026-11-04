"""Site outlines from the JRC Global Surface Water maximum water extent, and their HEALPix cells.

For each site in common.SITES: the JRC GSW v1.4 occurrence layer (1984-2021, Pekel et al. 2016, tile
30E_40N, read over HTTP for a 0.3 deg window) is thresholded at "water seen at least once", the connected
patch nearest the seed point is kept, buffered by 300 m (10 pixels), and its outline is covered with HEALPix
cells (depth 18, healpix-geo, WGS84). The same window also gives the JRC reference figures used in
02_analyse.py: maximum extent, permanent water (occurrence >= 90 %), and the JRC "transitions" class areas.

Usage: python pipeline/00_aoi.py <ROOT>          (ROOT = work)
Writes <ROOT>/aoi/<site>.geojson, <ROOT>/aoi/<site>_cells.npy and results/sites_jrc.json.
"""
import json
import os
import sys

import numpy as np
import rasterio
from rasterio import features
from rasterio.windows import from_bounds
from scipy import ndimage
import shapely
from shapely.geometry import shape, mapping

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

ROOT = sys.argv[1]
GSW = "/vsicurl/https://storage.googleapis.com/global-surface-water/downloads2021/{layer}/{layer}_30E_40Nv1_4_2021.tif"
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY="5", GDAL_HTTP_RETRY_DELAY="20")
HALF = 0.15
# JRC transitions classes (Pekel et al. 2016, data user guide v1.4)
TRANSITIONS = {1: "permanent", 2: "new permanent", 3: "lost permanent", 4: "seasonal", 5: "new seasonal",
               6: "lost seasonal", 7: "seasonal to permanent", 8: "permanent to seasonal",
               9: "ephemeral permanent", 10: "ephemeral seasonal"}


def read(layer, bounds):
    with rasterio.Env(**ENV), rasterio.open(GSW.format(layer=layer)) as r:
        w = from_bounds(*bounds, r.transform)
        return r.read(1, window=w), r.window_transform(w)


def pixel_area_ha(lat):
    return (0.00025 * 111320.0) ** 2 * np.cos(np.radians(lat)) / 1e4


def main():
    os.makedirs(f"{ROOT}/aoi", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    out = {}
    for key, s in common.SITES.items():
        b = (s["lon"] - HALF, s["lat"] - HALF, s["lon"] + HALF, s["lat"] + HALF)
        occ, tr = read("occurrence", b)
        water = (occ > 0) & (occ <= 100)
        lab, n = ndimage.label(water, structure=np.ones((3, 3)))
        r0, c0 = rasterio.transform.rowcol(tr, s["lon"], s["lat"])
        ys, xs = np.nonzero(lab)
        k = lab[ys, xs][np.argmin((ys - r0) ** 2 + (xs - c0) ** 2)]
        patch = lab == k
        buf = ndimage.binary_dilation(patch, iterations=10)
        geom = shapely.unary_union([shape(g) for g, v in features.shapes(buf.astype(np.uint8), transform=tr) if v == 1])
        geom = geom.buffer(0)
        ring = np.asarray(geom.exterior.coords) if geom.geom_type == "Polygon" else np.asarray(
            max(geom.geoms, key=lambda g: g.area).exterior.coords)
        cells = common.polygon_cells(ring[:-1])
        np.save(f"{ROOT}/aoi/{key}_cells.npy", cells)
        json.dump({"type": "Feature", "properties": {"site": key, **s}, "geometry": mapping(geom)},
                  open(f"{ROOT}/aoi/{key}.geojson", "w"))
        lat = s["lat"]
        tra, _ = read("transitions", b)
        pa = pixel_area_ha(lat)
        out[key] = {"name": s["name"], "why": s["why"], "seed": [s["lon"], s["lat"]],
                    "jrc_max_extent_ha": round(float(patch.sum() * pa), 1),
                    "jrc_permanent_ha_occ_ge90": round(float((patch & (occ >= 90)).sum() * pa), 1),
                    "jrc_mean_occurrence_pct": round(float(occ[patch].mean()), 1),
                    "jrc_transitions_ha": {TRANSITIONS[c]: round(float((patch & (tra == c)).sum() * pa), 1)
                                           for c in TRANSITIONS if (patch & (tra == c)).any()},
                    "healpix_cells": int(len(cells)), "healpix_area_ha": round(len(cells) * common.cell_area_ha(), 1),
                    "bbox": [round(v, 4) for v in geom.bounds]}
        print(key, json.dumps(out[key]), flush=True)
    json.dump({"source": "JRC Global Surface Water v1.4 (1984-2021), tile 30E_40N", "healpix_depth": common.DEPTH,
               "cell_area_ha": common.cell_area_ha(), "sites": out}, open("results/sites_jrc.json", "w"), indent=1)


if __name__ == "__main__":
    main()

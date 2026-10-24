"""The Konya Closed Basin on HEALPix: HydroBASINS level 4, HYBAS_ID 2040085960 (58,374 km2; Lehner and Grill 2013,
HydroSHEDS v1c, CC BY 4.0), as the depth-10 cells (healpix-geo, WGS84, NESTED) whose centre lies in the basin.
Cached in <ROOT>/wb/basin_cells.npy.
"""
import os

import geopandas as gpd
import healpix_geo.nested as hn
import numpy as np
import shapely

DEPTH = 10
HYBAS_ID = 2040085960


def polygon(root):
    g = gpd.read_file(f"zip://{root}/basin/hybas_eu_lev04.zip")
    return g[g.HYBAS_ID == HYBAS_ID].geometry.iloc[0]


def cells(root):
    fn = f"{root}/wb/basin_cells.npy"
    if os.path.exists(fn):
        return np.load(fn)
    b = polygon(root)
    x0, y0, x1, y1 = b.bounds
    ring = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
    ids, _, _ = hn.polygon_coverage(ring, DEPTH, ellipsoid="WGS84", flat=True)
    ids = np.unique(np.asarray(ids, np.uint64))
    lon, lat = hn.healpix_to_lonlat(ids, DEPTH, ellipsoid="WGS84")
    inside = shapely.contains_xy(b, np.asarray(lon), np.asarray(lat))
    out = np.sort(ids[inside])
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    np.save(fn, out)
    return out

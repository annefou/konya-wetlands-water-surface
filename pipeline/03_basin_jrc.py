"""Basin-wide change in surface water, Konya Closed Basin, from JRC Global Surface Water v1.4 transitions.

Basin: HydroBASINS level 4, endorheic basin HYBAS_ID 2040085960 (58,374 km2; Lehner and Grill 2013,
HydroSHEDS v1c, CC BY 4.0), containing Akgol, Tuz Golu, Beysehir and all six sites.
Transitions (Pekel et al. 2016) compare the first year (1984) with the last year (2021) of the record per
30 m pixel. Water in the first year = classes permanent, lost permanent, seasonal, lost seasonal, seasonal to
permanent, permanent to seasonal; water in the last year = permanent, new permanent, seasonal, new seasonal,
seasonal to permanent, permanent to seasonal (ephemeral classes excluded). Pixel area from latitude.
Reported for the whole basin and without Tuz Golu (salt crust; a lake whose surface the index method treats
differently). The basin's class counts are also aggregated onto HEALPix depth 13 (~0.8 km) with
healpix-resample ConservativeResampler (30 m pixels much smaller than the cells: binning is conservative).

Usage: python pipeline/03_basin_jrc.py <ROOT>
Writes results/basin_jrc.json and <ROOT>/basin/transitions_healpix13.parquet.
"""
import json
import os
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio import features
from rasterio.windows import from_bounds, Window
from shapely.geometry import Point

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

ROOT = sys.argv[1]
URL = "/vsicurl/https://storage.googleapis.com/global-surface-water/downloads2021/transitions/transitions_30E_40Nv1_4_2021.tif"
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY="5", GDAL_HTTP_RETRY_DELAY="20")
FIRST = [1, 3, 4, 6, 7, 8]
LAST = [1, 2, 4, 5, 7, 8]
TUZ = (33.292, 38.859)


def main():
    os.makedirs(f"{ROOT}/basin", exist_ok=True)
    import basin
    g = gpd.read_file(f"zip://{basin.download(ROOT)}")
    basin = g[g.HYBAS_ID == 2040085960].geometry.iloc[0]
    x0, y0, x1, y1 = basin.bounds
    first = last = 0.0
    first_nt = last_nt = 0.0
    by_class = {}
    hp_rows = []
    with rasterio.Env(**ENV), rasterio.open(URL) as r:
        win = from_bounds(x0, y0, x1, y1, r.transform).round_offsets().round_lengths()
        # strips of 1000 rows to keep memory bounded
        for row0 in range(int(win.row_off), int(win.row_off + win.height), 1000):
            w = Window(win.col_off, row0, win.width, min(1000, win.row_off + win.height - row0))
            a = r.read(1, window=w)
            tr = r.window_transform(w)
            inside = features.geometry_mask([basin], out_shape=a.shape, transform=tr, invert=True)
            rows = np.arange(a.shape[0])
            lat = tr.f + (rows + 0.5) * tr.e
            pa = ((0.00025 * 111320.0) ** 2 * np.cos(np.radians(lat)))[:, None] / 1e6        # km2
            pa = np.broadcast_to(pa, a.shape)
            # Tuz Golu: the JRC water patch connected to its centre, approximated by a 0.45 deg disc
            cols = np.arange(a.shape[1])
            lon = tr.c + (cols + 0.5) * tr.a
            LON, LAT = np.meshgrid(lon, lat)
            tuz = (LON - TUZ[0]) ** 2 + (LAT - TUZ[1]) ** 2 < 0.45 ** 2
            for c in range(1, 11):
                m = inside & (a == c)
                if m.any():
                    by_class[c] = by_class.get(c, 0.0) + float(pa[m].sum())
                    if c in FIRST:
                        first += float(pa[m].sum()); first_nt += float(pa[m & ~tuz].sum())
                    if c in LAST:
                        last += float(pa[m].sum()); last_nt += float(pa[m & ~tuz].sum())
            wm = inside & (a >= 1) & (a <= 10)
            if wm.any():
                hp_rows.append(pd.DataFrame({"lon": LON[wm], "lat": LAT[wm], "cls": a[wm], "km2": pa[wm]}))
    df = pd.concat(hp_rows)
    from healpix_resample import ConservativeResampler
    out = {}
    for name, cls in (("first_year_water_km2", FIRST), ("last_year_water_km2", LAST)):
        m = df.cls.isin(cls).values
        op = ConservativeResampler(lon_deg=df.lon.values[m], lat_deg=df.lat.values[m], level=13, nest=True,
                                   ellipsoid=common.ELLIPSOID, verbose=False)
        res = op.resample(df.km2.values[m])
        out[name] = pd.Series(np.asarray(res.cell_data, float), index=np.asarray(res.cell_ids, np.uint64))
    hp = pd.DataFrame(out).fillna(0.0)
    hp.index.name = "cell"
    hp.reset_index().to_parquet(f"{ROOT}/basin/transitions_healpix13.parquet", index=False)
    names = {1: "permanent", 2: "new permanent", 3: "lost permanent", 4: "seasonal", 5: "new seasonal",
             6: "lost seasonal", 7: "seasonal to permanent", 8: "permanent to seasonal", 9: "ephemeral permanent",
             10: "ephemeral seasonal"}
    res = {"basin": "HydroBASINS lev04 HYBAS_ID 2040085960", "basin_area_km2": round(float(g[g.HYBAS_ID == 2040085960].SUB_AREA.iloc[0])),
           "jrc_classes_km2": {names[c]: round(v, 1) for c, v in sorted(by_class.items())},
           "water_1984_km2": round(first, 1), "water_2021_km2": round(last, 1),
           "change_pct": round(100 * (last / first - 1), 1),
           "without_tuz_golu": {"water_1984_km2": round(first_nt, 1), "water_2021_km2": round(last_nt, 1),
                                "change_pct": round(100 * (last_nt / first_nt - 1), 1)},
           "healpix_check_km2": {"first": round(float(hp.first_year_water_km2.sum()), 1), "last": round(float(hp.last_year_water_km2.sum()), 1)},
           "paper_claim": "about -23.5 % (Musaoglu et al. 2018, Landsat 1987-2017, 16 water bodies)"}
    json.dump(res, open("results/basin_jrc.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

"""Konya Closed Basin water balance: is the wetland collapse a climate signal, and what does climate add to 2049?

Inputs: ERA5-Land monthly means 1990-2025 (04a_era5land_monthly.py) and Climate DT generation 2 monthly means
1990-2049 for IFS-FESOM and IFS-NEMO (04b_climatedt_monthly.py), all as basin means over the 1,442 depth-10 cells
of HydroBASINS 2040085960 (pipeline/basin.py). ERA5-Land (0.1 deg boxes, wider than a cell) is sampled onto the
cells with healpix-connector's coarse-grid sampler (value of the box containing the cell centre).
Water year = October to September, labelled by its ending year (1991 = Oct 1990 - Sep 1991).
1. ERA5-Land, water years 1991-2025: precipitation P, evaporation E (natural land surface: ERA5-Land has no
   irrigation), P - E, potential evaporation PET (atmospheric demand, a proxy of crop water need) and summer
   (June-August) temperature; Theil-Sen slope per decade with 95% interval, and 2016-2025 against 1991-2000.
2. Did the wetlands still fill in wet years? Spring fill (spring maximum as % of the 1984-1995 reference,
   results/site_years.csv) of the four sites that stopped filling, in the wettest third of water years
   1991-2005 against the wettest third of 2011-2025.
3. Climate DT: each model's 2040-2049 mean against its own 1991-2020 mean (changes only, as for the jerboa test),
   and its 1991-2020 bias against ERA5-Land.
Writes results/water_balance_annual.csv (basin means), results/water_balance_claims.json,
results/doc_figure_water_balance.json and figures/water_balance.png.
Usage: python pipeline/04c_water_balance.py <ROOT>
"""
import calendar
import glob
import json
import os
import sys

import numpy as np
import pandas as pd
import xarray as xr
from scipy.stats import theilslopes
from healpix_connector.sources.gridded import sample_cells_from_grid
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import basin  # noqa: E402

ROOT = sys.argv[1]
MODELS = ["IFS-FESOM", "IFS-NEMO"]
COLLAPSED = ["akgol", "hotamis", "meke", "meyil"]


def water_year(index):
    return index.year + (index.month >= 10)


def era5land(cells):
    ds = xr.open_dataset(f"{ROOT}/wb/era5land_monthly_1990_2025.nc")
    tv = "valid_time" if "valid_time" in ds.dims else "time"
    lat, lon = ds.latitude.values, ds.longitude.values
    if lat[0] < lat[-1]:
        ds = ds.isel(latitude=slice(None, None, -1)); lat = ds.latitude.values
    res = float(abs(lat[1] - lat[0]))
    t = pd.to_datetime(ds[tv].values)
    days = np.array([calendar.monthrange(x.year, x.month)[1] for x in t], float)
    out = {}
    for key, var, sign in (("P", "tp", 1), ("E", "e", -1), ("PET", "pev", -1)):
        a = ds[var].values * 1000.0 * sign * days[:, None, None]           # m per day -> mm per month
        out[key] = np.array([np.nanmean(sample_cells_from_grid(a[i], lon, lat, cells, basin.DEPTH, res).value)
                             for i in range(len(t))])
    a = ds["t2m"].values - 273.15
    out["T"] = np.array([np.nanmean(sample_cells_from_grid(a[i], lon, lat, cells, basin.DEPTH, res).value)
                         for i in range(len(t))])
    return pd.DataFrame(out, index=t)


def climatedt(model):
    rows = []
    for f in sorted(glob.glob(f"{ROOT}/wb/dt_{model}/*.npz")):
        y = int(os.path.basename(f)[:4]); d = np.load(f)
        for m in range(12):
            rows.append({"time": pd.Timestamp(y, m + 1, 1), "P": float(d["pr"][m].mean()), "E": float(d["evap"][m].mean()),
                         "T": float(d["t2m"][m].mean())})
    return pd.DataFrame(rows).set_index("time")


def annual(m):
    wy = water_year(m.index)
    a = m.groupby(wy).agg({c: ("mean" if c == "T" else "sum") for c in m.columns if c != "T"} | {})
    a["P-E"] = a["P"] - a["E"]
    a["T_JJA"] = m["T"][m.index.month.isin([6, 7, 8])].groupby(m.index.year[m.index.month.isin([6, 7, 8])]).mean()
    n = m.groupby(wy).size()
    return a[n == 12]


def slope(s):
    s = s.dropna()
    r = theilslopes(s.values, s.index.values)
    return {"per_decade": round(10 * r[0], 2), "ci95": [round(10 * r[2], 2), round(10 * r[3], 2)]}


def main():
    os.makedirs("results", exist_ok=True)
    cells = basin.cells(ROOT)
    e5 = annual(era5land(cells)).loc[1991:2025]
    claims = {"basin_cells": int(len(cells)), "era5land_water_years_1991_2025": {}, "wet_year_fill": {}, "climatedt": {}}
    for c in ["P", "E", "P-E", "PET", "T_JJA"]:
        early, late = e5[c].loc[1991:2000].mean(), e5[c].loc[2016:2025].mean()
        claims["era5land_water_years_1991_2025"][c] = {
            "mean_1991_2020": round(float(e5[c].loc[1991:2020].mean()), 1), "theil_sen": slope(e5[c]),
            "mean_1991_2000": round(float(early), 1), "mean_2016_2025": round(float(late), 1),
            "change": round(float(late - early), 1) if c == "T_JJA" else round(float(100 * (late / early - 1)), 1)}
    # 2. wet years and spring fill
    sy = pd.read_csv("results/site_years.csv")
    sy["pct"] = 100 * sy.spring_max_ha / sy.ref_spring_ha
    fill = sy[sy.site.isin(COLLAPSED)].groupby("year").pct.mean()
    for (a, b) in ((1991, 2005), (2011, 2025)):
        p = e5["P"].loc[a:b]
        wet = p[p >= p.quantile(2 / 3)].index
        f = fill.reindex(wet).dropna()
        claims["wet_year_fill"][f"{a}-{b}"] = {"wet_years": [int(y) for y in wet],
                                               "precip_mm": [round(float(e5.loc[y, "P"])) for y in wet],
                                               "mean_spring_fill_pct_4_sites": round(float(f.mean()), 1),
                                               "years_with_fill_data": int(len(f))}
    # 3. Climate DT
    dt = {}
    for m in MODELS:
        a = annual(climatedt(m))
        dt[m] = a
        base, fut = a.loc[1991:2020], a.loc[2040:2049]
        claims["climatedt"][m] = {
            "bias_1991_2020_vs_era5land": {"P_pct": round(float(100 * (base.P.mean() / e5.P.loc[1991:2020].mean() - 1)), 1),
                                           "E_pct": round(float(100 * (base.E.mean() / e5.E.loc[1991:2020].mean() - 1)), 1),
                                           "T_JJA_degC": round(float(base.T_JJA.mean() - e5.T_JJA.loc[1991:2020].mean()), 2)},
            "change_2040s_vs_1991_2020": {"P_pct": round(float(100 * (fut.P.mean() / base.P.mean() - 1)), 1),
                                          "E_pct": round(float(100 * (fut.E.mean() / base.E.mean() - 1)), 1),
                                          "P-E_mm": round(float(fut["P-E"].mean() - base["P-E"].mean()), 1),
                                          "T_JJA_degC": round(float(fut.T_JJA.mean() - base.T_JJA.mean()), 2)}}
    json.dump(claims, open("results/water_balance_claims.json", "w"), indent=1)
    print(json.dumps(claims, indent=1))
    tab = [e5.assign(source="ERA5-Land")] + [dt[m].assign(source=f"Climate DT {m}") for m in MODELS]
    out = pd.concat(tab).rename_axis("water_year").reset_index().round(2)
    out.to_csv("results/water_balance_annual.csv", index=False)
    rows = [{"year": int(y), "precip_pct": round(float(100 * e5.loc[y, "P"] / e5.P.loc[1991:2020].mean())),
             "fill_pct": (None if y not in fill.index else round(float(min(fill.loc[y], 150))))} for y in e5.index]
    json.dump(rows, open("results/doc_figure_water_balance.json", "w"), indent=1)

    fig, axs = plt.subplots(2, 1, figsize=(10, 5.6), sharex=True)
    axs[0].bar(e5.index, 100 * e5.P / e5.P.loc[1991:2020].mean(), color="#9fb7d9")
    axs[0].axhline(100, color="0.4", lw=0.8)
    axs[0].set_ylabel("Water-year precipitation\n(% of 1991-2020)")
    axs[1].plot(fill.loc[1991:].index, fill.loc[1991:].clip(upper=150), "-o", color="#2f6fd6", ms=3)
    axs[1].axhline(50, color="0.4", lw=0.8, ls="--")
    axs[1].set_ylabel("Spring fill, 4 sites\n(% of 1984-1995)")
    for ax in axs:
        ax.spines[["top", "right"]].set_visible(False)
    axs[0].set_title("Konya Closed Basin: rain did not fall away, the wetlands did (ERA5-Land; Landsat)", loc="left", fontsize=10)
    fig.tight_layout(); fig.savefig("figures/water_balance.png", dpi=160); plt.close(fig)


if __name__ == "__main__":
    main()

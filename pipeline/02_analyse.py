"""Claims tested against the per-scene Landsat series (01_landsat_scenes.py), NDWI > 0 unless stated.

C1 (Musaoglu et al. 2018) Akgol water surface 2958.4 ha (1987), 1153.9 ha (1998), 12.7 ha (2007),
   117.2 ha (2017), one image per year: every valid scene of those years, the paper's value set against
   their range, and the scene closest to it.
C2 (Ozgencil et al. 2025) wetlands dry earlier in the season over 1998-2018: per site and year, the drying
   date = first valid scene after day 100 whose water area is at most 10 % of the site's reference spring
   area (median of April-May scenes, 1984-1995); years in which the site never falls that low are kept as
   "not dry" (censored at day 366). Compared as medians of 1996-2000 against 2016-2020, plus a Theil-Sen
   slope over all years.
Also per site and year: spring maximum (March-June) and late-summer median (July-September).

Usage: python pipeline/02_analyse.py <ROOT>
Writes results/akgol_paper_years.csv, results/site_years.csv, results/claims.json, figures/*.png.
"""
import json
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import theilslopes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

ROOT = sys.argv[1]
COL = "water_ha_ndwi_+0.0"
PAPER = {1987: 2958.4, 1998: 1153.9, 2007: 12.7, 2017: 117.2}


def load():
    d = pd.read_csv(f"{ROOT}/landsat/scenes.csv")
    d["date"] = pd.to_datetime(d.datetime, utc=True).dt.tz_convert(None)
    d = d[d[COL].notna() & (d[COL] != "")].copy()
    for c in [c for c in d.columns if c.startswith("water_ha")]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["year"], d["doy"] = d.date.dt.year, d.date.dt.dayofyear
    return d.sort_values("date")


def drying(d):
    rows = []
    for site, g in d.groupby("site"):
        ref = g[(g.year <= 1995) & g.date.dt.month.isin([4, 5])][COL].median()
        for y, gy in g.groupby("year"):
            spring = gy[gy.date.dt.month.isin([3, 4, 5, 6])][COL]
            summer = gy[gy.date.dt.month.isin([7, 8, 9])][COL]
            after = gy[gy.doy > 100]
            dry = after[after[COL] <= 0.1 * ref]
            rows.append({"site": site, "year": y, "n_scenes": len(gy), "ref_spring_ha": round(ref, 1),
                         "spring_max_ha": round(spring.max(), 1) if len(spring) else np.nan,
                         "summer_median_ha": round(summer.median(), 1) if len(summer) else np.nan,
                         "drying_doy": int(dry.doy.iloc[0]) if len(dry) else (366 if len(after) >= 4 else np.nan)})
    return pd.DataFrame(rows)


def main():
    os.makedirs("results", exist_ok=True)
    os.makedirs("figures", exist_ok=True)
    d = load()
    ak = d[d.site == "akgol"]
    py = []
    for y, v in PAPER.items():
        g = ak[ak.year == y]
        if not len(g):
            py.append({"year": y, "paper_ha": v, "n_scenes": 0}); continue
        k = (g[COL] - v).abs().idxmin()
        py.append({"year": y, "paper_ha": v, "n_scenes": len(g), "min_ha": g[COL].min(), "median_ha": g[COL].median(),
                   "max_ha": g[COL].max(), "closest_date": str(g.loc[k, "date"].date()), "closest_ha": g.loc[k, COL],
                   "paper_within_range": bool(g[COL].min() <= v <= g[COL].max()),
                   "spread_thr_-0.1_+0.1_at_closest": [g.loc[k, "water_ha_ndwi_-0.1"], g.loc[k, "water_ha_ndwi_+0.1"]]})
    py = pd.DataFrame(py)
    py.to_csv("results/akgol_paper_years.csv", index=False)
    sy = drying(d)
    sy.to_csv("results/site_years.csv", index=False)
    claims = {"C1_akgol_paper_years": py.to_dict(orient="records"), "C2_drying": {}, "series": {}}
    for site, g in sy.groupby("site"):
        early = g[g.year.between(1996, 2000)].drying_doy.median()
        late = g[g.year.between(2016, 2020)].drying_doy.median()
        ok = g.dropna(subset=["drying_doy"])
        slope = theilslopes(ok.drying_doy, ok.year) if len(ok) > 8 else None
        sm = g.dropna(subset=["spring_max_ha"])
        claims["C2_drying"][site] = {"median_doy_1996_2000": early, "median_doy_2016_2020": late,
                                     "change_days": None if np.isnan(early) or np.isnan(late) else float(late - early),
                                     "theil_sen_days_per_decade": None if slope is None else round(10 * slope[0], 1),
                                     "ci95": None if slope is None else [round(10 * slope[2], 1), round(10 * slope[3], 1)],
                                     "years_used": int(len(ok))}
        claims["series"][site] = {"years": int(g.year.nunique()), "scenes": int(g.n_scenes.sum()),
                                  "spring_max_1984_1995_median_ha": float(sm[sm.year <= 1995].spring_max_ha.median()),
                                  "spring_max_2015_2025_median_ha": float(sm[sm.year >= 2015].spring_max_ha.median())}
    json.dump(claims, open("results/claims.json", "w"), indent=1, default=float)
    print(py.to_string(index=False))
    print(json.dumps(claims["C2_drying"], indent=1, default=float))
    print(json.dumps(claims["series"], indent=1, default=float))

    # Figure 1: Akgol, every valid scene, with the paper's four values
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.scatter(ak.date, ak[COL], s=8, color="0.55", label="Every valid Landsat scene (NDWI > 0, HEALPix cells)")
    ax.scatter([pd.Timestamp(f"{y}-07-01") for y in PAPER], list(PAPER.values()), s=60, marker="D",
               color="#1f5fbf", zorder=3, label="Musaoğlu et al. 2018 (one image per year; date not stated)")
    ax.set_ylabel("Water surface (ha)")
    ax.set_title("Akgöl: one image a year hides a two-fold seasonal range")
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig("figures/akgol_scenes.png", dpi=160); plt.close(fig)

    # Figure 2: spring maximum per site and year
    sites = list(common.SITES)
    fig, axs = plt.subplots(2, 3, figsize=(11, 5.5), sharex=True)
    for ax, s in zip(axs.ravel(), sites):
        g = sy[sy.site == s]
        ax.plot(g.year, g.spring_max_ha, color="#1f5fbf", lw=1.2, label="Spring maximum")
        ax.plot(g.year, g.summer_median_ha, color="0.6", lw=1.2, label="Late-summer median")
        ax.set_title(common.SITES[s]["name"], fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
    axs[0, 0].set_ylabel("Water surface (ha)"); axs[1, 0].set_ylabel("Water surface (ha)")
    axs[0, 0].legend(frameon=False, fontsize=8)
    fig.suptitle("Konya Closed Basin wetlands, Landsat 1984-2025 (NDWI > 0 on HEALPix cells)")
    fig.tight_layout(); fig.savefig("figures/sites_spring_summer.png", dpi=160); plt.close(fig)

    # Figure 3: drying date per site and year
    fig, axs = plt.subplots(2, 3, figsize=(11, 5.5), sharex=True, sharey=True)
    for ax, s in zip(axs.ravel(), sites):
        g = sy[sy.site == s]
        ax.scatter(g.year, g.drying_doy, s=10, color="#1f5fbf")
        ax.axhline(366, color="0.8", lw=0.8)
        ax.set_title(common.SITES[s]["name"], fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
    axs[0, 0].set_ylabel("Day of year"); axs[1, 0].set_ylabel("Day of year")
    fig.suptitle("Drying date: first scene at or below 10 % of the 1984-1995 spring area (366 = did not dry)")
    fig.tight_layout(); fig.savefig("figures/sites_drying_doy.png", dpi=160); plt.close(fig)


if __name__ == "__main__":
    main()

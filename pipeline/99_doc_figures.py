"""Rows of the figures shown in the LifeWatch ERIC country file for Turkiye, from the pipeline outputs.

1. results/doc_figure_fill.json: spring maximum water surface per site and year as % of the site's
   1984-1995 spring reference (results/site_years.csv), capped at 200 %.
2. results/akgol_scenes.csv: water surface of Akgol in every valid Landsat scene (NDWI > 0), from
   <ROOT>/landsat/scenes.csv; Landsat Collection 2 is public domain, so the per-scene areas are committed.
3. figures/doc_fill.png: figure 1 as PNG.
4. results/doc_figure_akgol_scenes.csv: rows of figure 2 (date, decimal year, water surface in ha).
Usage: python pipeline/99_doc_figures.py <ROOT>
"""
import json
import sys

import pandas as pd

ROOT = sys.argv[1]
NAMES = {"akgol": "Akgöl", "hotamis": "Hotamış", "meke": "Meke (Ramsar)", "meyil": "Meyil", "bolluk": "Bolluk",
         "acigol_k": "Acıgöl–Karapınar (control)"}
COLLAPSED = {"akgol", "hotamis", "meke", "meyil"}   # did not fill in any year of the 2020s (results/fill_by_decade.csv)
sy = pd.read_csv("results/site_years.csv").dropna(subset=["spring_max_ha", "ref_spring_ha"])
rows = [{"site": NAMES[r.site], "year": int(r.year), "pct": round(min(100 * r.spring_max_ha / r.ref_spring_ha, 200), 1),
         "collapsed": int(r.site in COLLAPSED), "order": list(NAMES).index(r.site)} for r in sy.itertuples()]
rows.sort(key=lambda r: (r["order"], r["year"]))
json.dump(rows, open("results/doc_figure_fill.json", "w"), indent=1, ensure_ascii=False)
s = pd.read_csv(f"{ROOT}/landsat/scenes.csv")
s = s[(s.site == "akgol") & s["water_ha_ndwi_+0.0"].notna()].copy()
s["date"] = s.datetime.str[:10]
s = s.sort_values("date")[["date", "scene", "platform", "valid_share", "water_ha_ndwi_-0.1", "water_ha_ndwi_+0.0", "water_ha_ndwi_+0.1"]]
s.to_csv("results/akgol_scenes.csv", index=False)
# rows of figure 2 (Akgol, every valid scene, beside the paper's four values): date as a decimal year and the area
s2 = s[["date", "water_ha_ndwi_+0.0"]].rename(columns={"water_ha_ndwi_+0.0": "water_ha"})
d = pd.to_datetime(s2.date)
s2.insert(1, "t", (d.dt.year + (d.dt.dayofyear - 1) / 365.25).round(3))
s2["water_ha"] = s2.water_ha.round(1)
s2.to_csv("results/doc_figure_akgol_scenes.csv", index=False)
print(len(rows), "fill rows;", len(s), "Akgol scenes")

# The country-file figure as PNG, drawn from the same rows (the country file draws it live from them).
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CAP = 150      # display cap, as in the country file
fig, axs = plt.subplots(2, 3, figsize=(11, 5.6), sharey=True)
for ax, (site, name) in zip(axs.ravel(), NAMES.items()):
    g = [r for r in rows if r["site"] == name]
    c = "#2f6fd6" if site in COLLAPSED else "#b8b8b0"
    ax.plot([r["year"] for r in g], [min(r["pct"], CAP) for r in g], "-o", color=c, ms=3, lw=1.6)
    ax.axhline(50, color="0.45", lw=0.8, ls="--")
    ax.set_title(name, fontsize=10, fontweight="bold", loc="left")
    ax.set_ylim(0, CAP + 5); ax.set_yticks([0, 50, 100], ["0", "50%", "100%"])
    ax.spines[["top", "right"]].set_visible(False)
fig.suptitle("Akgöl, Hotamış, Meke and Meyil no longer fill in spring; the control lake is stable",
             x=0.01, ha="left", fontweight="bold")
fig.text(0.01, 0.905, f"Spring maximum water surface each year, % of the site's 1984-1995 median spring maximum "
         f"(Landsat, NDWI on HEALPix cells; capped at {CAP}%). Dashed: 50%, counted as filled.", fontsize=8.5, color="0.35")
fig.tight_layout(rect=(0, 0, 1, 0.89))
fig.savefig("figures/doc_fill.png", dpi=160); plt.close(fig)

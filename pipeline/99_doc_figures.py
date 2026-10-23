"""Rows of the figures shown in the LifeWatch ERIC country file for Turkiye, from the pipeline outputs.

1. results/doc_figure_fill.json: spring maximum water surface per site and year as % of the site's
   1984-1995 spring reference (results/site_years.csv), capped at 200 %.
2. results/akgol_scenes.csv: water surface of Akgol in every valid Landsat scene (NDWI > 0), from
   <ROOT>/landsat/scenes.csv; Landsat Collection 2 is public domain, so the per-scene areas are committed.
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
print(len(rows), "fill rows;", len(s), "Akgol scenes")

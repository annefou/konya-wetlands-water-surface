# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 01 — Data
#
# **DRAFT, not reviewed.** LifeWatch ERIC feasibility test, our reading of the published work, open to correction by
# the authors.
#
# The pipeline is in `pipeline/` and `Snakefile` (see *How to reproduce* in the README). It is **not** rerun when this
# book is built: the Landsat step takes about 40 minutes, and the water-balance step needs a CDS account (ERA5-Land) and
# DestinE upgraded access (Climate DT). These pages read the summary results committed in `results/` and the figures
# in `figures/`.
#
# | Input | Source | Licence | Pipeline step |
# |---|---|---|---|
# | Landsat Collection 2 Level-2 (Landsat 5, 7, 8, 9), every valid scene 1984–2025 | Microsoft Planetary Computer, anonymous | USGS, public domain | `pipeline/01_landsat_scenes.py` |
# | JRC Global Surface Water v1.4 (1984–2021) | JRC | CC BY 4.0 | `pipeline/00_aoi.py`, `pipeline/03_basin_jrc.py` |
# | HydroBASINS level 4, endorheic basin 2040085960 (58,374 km²) | HydroSHEDS | CC BY 4.0 | `pipeline/03_basin_jrc.py`, `pipeline/basin.py` |
# | OpenStreetMap seed points for the wetlands | OSM | ODbL | `pipeline/00_aoi.py` |
# | ERA5-Land monthly means | Copernicus CDS (account) | Copernicus licence | `pipeline/04a_era5land_monthly.py` |
# | Climate DT generation 2 monthly means, IFS-FESOM and IFS-NEMO, 1990–2049 | DestinE upgraded access | DestinE terms: raw data not redistributed, basin means only | `pipeline/04b_climatedt_monthly.py` |
#
# Grid: HEALPix on the WGS84 ellipsoid (healpix-geo), NESTED; depth 18 (~25 m) for Landsat, depth 10 for the basin.

# %%
import json
from pathlib import Path

import pandas as pd

R = Path("../results")
sites = json.loads((R / "sites_jrc.json").read_text())
print(sites["source"], "| HEALPix depth", sites["healpix_depth"], f"| cell area {sites['cell_area_ha']:.3f} ha")
pd.DataFrame([{"site": k, "name": v["name"], "why": v.get("why", ""), "JRC max extent (ha)": v["jrc_max_extent_ha"],
               "HEALPix cells": v["healpix_cells"]} for k, v in sites["sites"].items()])

# %%
# Committed results (summary statistics only; downloads stay in work/, which is not in git)
pd.DataFrame([{"file": f.name, "bytes": f.stat().st_size} for f in sorted(R.iterdir()) if f.is_file()])

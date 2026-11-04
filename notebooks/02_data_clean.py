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
# # 02 — Scenes and masking
#
# Each Landsat scene: green, NIR and QA_PIXEL are read for the site window; cloud, shadow, snow and fill are masked;
# green and NIR are resampled onto HEALPix depth-17 cells with healpix-resample (conservative bilinear) **before**
# NDWI and its threshold (NDWI > 0; −0.1 and +0.1 as sensitivity). A scene counts for a site when at least 95 % of
# its cells are valid.
#
# Gaps: 2012–2013 has no valid scene (end of Landsat 5, before Landsat 8; Landsat 7 scan-line gaps fail the 95 %
# rule). Two 2022 scenes could not be read and are excluded.

# %%
from pathlib import Path

import pandas as pd

R = Path("../results")
scenes = pd.read_csv(R / "akgol_scenes.csv")
print(len(scenes), "valid Akgöl scenes")
scenes.head()

# %%
sy = pd.read_csv(R / "site_years.csv")
print(sy.columns.tolist())
sy.head(10)

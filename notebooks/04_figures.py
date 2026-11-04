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
# # 04 — Figures
#
# Written by the pipeline (`pipeline/02_analyse.py`, `pipeline/04c_water_balance.py`, `pipeline/99_doc_figures.py`)
# and committed in `figures/`.

# %% [markdown]
# ## Akgöl: every valid scene against the paper's four values
# One image per year hides a two-fold seasonal range (3,860 ha on 22 April and 1,969 ha on 27 July 1987).
# ![Akgöl, every scene](../figures/akgol_scenes.png)
#
# ## Spring and summer water surface per site
# ![Spring and summer per site](../figures/sites_spring_summer.png)
#
# ## Drying date per site
# ![Drying date](../figures/sites_drying_doy.png)
#
# ## Share of years each wetland fills, per decade
# ![Fill by decade](../figures/doc_fill.png)
#
# ## Basin water balance and wetland filling
# ![Water balance](../figures/water_balance.png)

# %% [markdown]
# ## Limits
# - NDWI misses bright or turbid water in some scenes (Acıgöl reads 0 ha from January to June 1996), so the reference
#   is the median of yearly spring maxima, not single scenes. MNDWI would be more robust for the crater lakes; the
#   replication keeps the paper's NDWI.
# - NDWI on salt crust and shallow turbid water is uncertain; Tuz Gölü is separated with a 0.45° circle.
# - Water surface only: no depth, salinity or ecological condition.

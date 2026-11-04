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
# # 03 — Claims tested
#
# | Claim | Source | Our test |
# |---|---|---|
# | C1. Akgöl water surface 2958.4 ha (1987), 1153.9 (1998), 12.7 (2007), 117.2 (2017); about −96 % | Musaoğlu et al. 2018, [doi:10.17501/iccc.2018.2102](https://doi.org/10.17501/iccc.2018.2102), one Landsat image per year, NDWI | Every valid Landsat scene of those years, same index |
# | C2. Konya Closed Basin water bodies about −23.5 % over 30 years | Musaoğlu et al. 2018 | JRC Global Surface Water transitions 1984–2021 over the HydroBASINS endorheic basin |
# | C3. Wetlands dry earlier in the season (1998–2018) | Özgencil et al. 2025, [doi:10.1080/20442041.2025.2488655](https://doi.org/10.1080/20442041.2025.2488655) | Share of years each wetland still fills in spring, per decade, 1984–2025 |

# %% [markdown]
# ## C1 — Akgöl in the paper's four years
# The paper's image dates are not stated, so the paper value is compared with the range of all valid scenes of each
# year. Reproduced for 1987, 2007 and 2017; not for 1998.

# %%
import json
from pathlib import Path

import pandas as pd

R = Path("../results")
claims = json.loads((R / "claims.json").read_text())
pd.DataFrame(claims["C1_akgol_paper_years"])

# %% [markdown]
# ## Grid depth: why HEALPix depth 18
# The same Landsat pixels at depth 17 (~50 m), depth 18 (~25 m) and as native 30 m pixels counted inside the
# outline (`pipeline/91_depth_sensitivity.py`). Depth 17, coarser than the pixel, under-counted small or patchy water;
# the replication uses depth 18. Differences in % against the native pixels, scenes with at least 1 ha of water.

# %%
ds = json.loads((R / "depth_sensitivity.json").read_text())["sites"]
pd.DataFrame({k: {"scenes": v["scenes"], "depth 17 vs native, median %": v["ha_d17_vs_native_pct"]["median"],
                  "depth 18 vs native, median %": v["ha_d18_vs_native_pct"]["median"]} for k, v in ds.items()}).T

# %% [markdown]
# ## C2 — basin water, JRC 1984 → 2021
# Tuz Gölü, a shallow salt lake holding about 40 % of the basin's water, hides the loss of the freshwater lakes and
# wetlands.

# %%
b = json.loads((R / "basin_jrc.json").read_text())
pd.DataFrame([{"scope": "whole basin", "1984 (km²)": b["water_1984_km2"], "2021 (km²)": b["water_2021_km2"],
               "change (%)": b["change_pct"]},
              {"scope": "without Tuz Gölü", "1984 (km²)": b["without_tuz_golu"]["water_1984_km2"],
               "2021 (km²)": b["without_tuz_golu"]["water_2021_km2"], "change (%)": b["without_tuz_golu"]["change_pct"]}])

# %% [markdown]
# ## C3 — share of years each wetland still fills in spring
# A year counts as filled when its spring maximum reaches half the 1984–1995 median spring maximum. Acıgöl
# (Karapınar), a crater lake, is the control.

# %%
fill = pd.read_csv(R / "fill_by_decade.csv")
fill.pivot(index="site", columns="decade", values="fill_share").round(2)

# %% [markdown]
# ## Basin water balance: climate or water use?
# ERA5-Land water years 1991–2025 and Climate DT generation 2 (2040s), basin means over 1,442 depth-10 cells.
# ERA5-Land has no irrigation; groundwater and irrigated-area data would be needed to test the water-use explanation.

# %%
wb = json.loads((R / "water_balance_claims.json").read_text())
era = wb["era5land_water_years_1991_2025"]
pd.DataFrame({k: {"mean 1991–2020": v.get("mean_1991_2020"), "Theil–Sen per decade": v["theil_sen"]["per_decade"],
                  "95 % CI": v["theil_sen"]["ci95"], "change (%)": v.get("change")}
              for k, v in era.items() if isinstance(v, dict) and "theil_sen" in v}).T

# %%
print(json.dumps({k: v for k, v in wb.items() if k != "era5land_water_years_1991_2025"}, indent=1, ensure_ascii=False))

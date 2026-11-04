# konya-wetlands-water-surface

[![CI](https://github.com/annefou/konya-wetlands-water-surface/actions/workflows/ci.yml/badge.svg)](https://github.com/annefou/konya-wetlands-water-surface/actions/workflows/ci.yml)
[![Jupyter Book](https://github.com/annefou/konya-wetlands-water-surface/actions/workflows/jupyter-book.yml/badge.svg)](https://annefou.github.io/konya-wetlands-water-surface/)
[![Docker](https://github.com/annefou/konya-wetlands-water-surface/actions/workflows/docker.yml/badge.svg)](https://github.com/annefou/konya-wetlands-water-surface/pkgs/container/konya-wetlands-water-surface)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23942467.svg)](https://doi.org/10.5281/zenodo.23942467)
[![FAIR4RS](https://img.shields.io/badge/FAIR4RS-conformant-brightgreen)](docs/fair4rs-checklist.md)
[![FORRT](https://img.shields.io/badge/FORRT-replication-blue)](https://forrt.org/)
[![Science Live](https://img.shields.io/badge/Science%20Live-nanopub%20chain-purple)](nanopubs/PUBLISHED.md)
[![RO-Crate](https://img.shields.io/badge/RO--Crate-1.2-orange)](ro-crate-metadata.json)
[![Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/annefou/konya-wetlands-water-surface/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/annefou/konya-wetlands-water-surface)

> **Long-Term Monitoring of Wetlands via Remote Sensing and GIS: A Case Study from Turkey** — replication study.
> Reference paper: [10.17501/iccc.2018.2102](https://doi.org/10.17501/iccc.2018.2102)

**DRAFT, not reviewed.** LifeWatch ERIC feasibility test prepared for the meeting with HUBIOM (Hacettepe University) on 30 October 2026. Our reading of the published work, open to correction by the authors.

### Claims tested

| Claim | Source | Our test |
| --- | --- | --- |
| C1. Akgöl water surface 2958.4 ha (1987), 1153.9 (1998), 12.7 (2007), 117.2 (2017); about -96 % | Musaoğlu et al. 2018, one Landsat image per year, NDWI | Every valid Landsat scene of those years, same index |
| C2. Konya Closed Basin water bodies about -23.5 % over 30 years | Musaoğlu et al. 2018 | JRC Global Surface Water transitions 1984-2021 over the HydroBASINS endorheic basin |
| C3. Wetlands dry earlier in the season (1998-2018) | Özgencil et al. 2025, [doi:10.1080/20442041.2025.2488655](https://doi.org/10.1080/20442041.2025.2488655) | Share of years each wetland still fills in spring, per decade, 1984-2025 |

### Results (23 October 2026)

- **C1 reproduced for 1987, 2007 and 2017**: the scene closest to the paper's value is 3007 ha on 9 June 1987 (paper 2958.4), 9.3 ha on 31 May 2007 (12.7), 94.8 ha on 27 June 2017 (117.2), and the paper's values lie within the range of each year's valid scenes. For 1998 our valid scenes peak at 828 ha, below the paper's 1153.9 ha at its threshold (NDWI > 0); at NDWI > -0.1 the same scene gives 1152 ha. One image per year hides a two-fold seasonal range: 3,860 ha on 22 April and 1,969 ha on 27 July 1987.
- **C2 consistent**: JRC water 2,540 km2 (1984) -> 2,033 km2 (2021), **-20.0 %**; without Tuz Gölü, **-40.4 %** (1,477 -> 880 km2). Tuz Gölü, a shallow salt lake holding 40 % of the basin's water, hides the loss of the freshwater lakes and wetlands.
- **C3 supported, in a stronger form** (a year counts as filled when its spring maximum reaches half the 1984-1995 median spring maximum): Akgöl filled in every year of the 1980s, 40 % of the 1990s, never since 2000 (spring maximum 3,423 -> 299 ha, 1984-95 vs 2015-25 medians); Hotamış 1,254 -> 25 ha, never since 2010; Meke (Ramsar) 55 -> 3 ha, never in the 2020s; Meyil 7.8 -> 2.7 ha, 78 % of the 2010s and never in the 2020s. The crater lake Acıgöl (Karapınar) is stable (111 -> 99 ha) and serves as a control. Table: `results/fill_by_decade.csv`.
- **Grid depth** (`pipeline/91_depth_sensitivity.py`, `results/depth_sensitivity.json`): until 4 November 2026 the
  cells were depth 17 (~50 m), coarser than the 30 m pixels. Against the native pixels, depth 17 under-counted small or
  patchy water (median -17 % at Akgöl, -23 % at Meyil, scenes with at least 1 ha of water); depth 18 (~25 m) gives
  -4.5 % and -6.9 %, so the replication now uses depth 18. Large extents agree at both depths (1987: 2999, 3007 and
  2997 ha). C3 (fill by decade) and the wet-year fill are unchanged; C1's closest scenes and the 1996-2000 drying date
  at Akgöl changed (numbers above are depth 18).
- **NDWI caveat**: NDWI misses bright or turbid water in some scenes (Acıgöl reads 0 ha from January to June 1996; Meyil reads 0 in some scenes); the reference is therefore the median of yearly spring maxima, not of single scenes. MNDWI (SWIR) would be more robust for the crater lakes; the replication keeps the paper's NDWI.

Figures: [Akgöl, every scene](figures/akgol_scenes.png) · [spring and summer per site](figures/sites_spring_summer.png) · [drying date](figures/sites_drying_doy.png). Tables: `results/`.

### Method

- Landsat Collection 2 Level-2 (Landsat 5, 7, 8, 9) from Microsoft Planetary Computer, anonymous access. Each scene: green, NIR and QA_PIXEL read for the site window; cloud, shadow, snow and fill masked; green and NIR resampled onto HEALPix cells (depth 18, ~25 m, [healpix-geo](https://github.com/GRID4EARTH/healpix-geo) on the WGS84 ellipsoid, NESTED) with [healpix-resample](https://github.com/GRID4EARTH/healpix-resample) (conservative bilinear) **before** NDWI and its threshold (NDWI > 0; -0.1 and +0.1 as sensitivity). A scene counts for a site when at least 95 % of its cells are valid.
- Site outlines: JRC Global Surface Water v1.4 maximum extent around seed points checked on OpenStreetMap.
- Basin: HydroBASINS level 4, endorheic basin 2040085960 (58,374 km2).

### Basin water balance: climate or water use?

`pipeline/04a_era5land_monthly.py` (ERA5-Land monthly means, CDS), `pipeline/04b_climatedt_monthly.py` (Climate DT generation 2 monthly means, IFS-FESOM and IFS-NEMO, 1990-2049, region cut out by Polytope, sphere -> WGS84 with healpix-connector) and `pipeline/04c_water_balance.py` compute the natural water balance of HydroBASINS 2040085960 on 1,442 depth-10 cells (`pipeline/basin.py`). Water years 1991-2025: precipitation -10% (not significant), summer temperature +0.49 degC and potential evaporation +33 mm per decade; in the wettest third of years the four collapsed wetlands filled to 67% (1991-2005) and 23% (2011-2025) of their 1984-1995 level (the same with one fixed threshold for both periods, the wettest third of the 1991-2020 normal: 67% and 22%, 2017 dropping out). Climate DT 2040s: precipitation -14 to -16%, summers +2.3 to +2.9 degC. ERA5-Land has no irrigation; groundwater and irrigated-area data would test the water-use explanation. Results: `results/water_balance_claims.json`; only basin means are committed (DestinE terms).

### Limits

- The paper's image dates are not stated; we compare with the range of all valid scenes in each year.
- 2012-2013 has no valid scenes (end of Landsat 5, before Landsat 8; Landsat 7 scan-line gaps fail the 95 % rule). Two 2022 scenes could not be read and are excluded.
- NDWI on salt crust and on shallow turbid water is uncertain; Tuz Gölü is separated with a 0.45 deg circle.
- Water surface only: no depth, salinity or ecological condition.

### Data

Landsat (USGS, public domain), JRC Global Surface Water (CC BY 4.0), HydroBASINS (CC BY 4.0), OpenStreetMap (ODbL, seed points only). Only code, plots and summary statistics are in this repository; inputs are fetched by the pipeline.

---

## Install and run

You can read the results without installing anything: the summary tables are in `results/`, the figures in
`figures/`, and the [Jupyter Book](https://annefou.github.io/konya-wetlands-water-surface/) shows both. Rerunning the analysis needs the
steps below.

### Install

1. Install pixi (<https://pixi.sh>): `curl -fsSL https://pixi.sh/install.sh | bash`.
2. Get the code and the pinned environment:

   ```bash
   git clone https://github.com/annefou/konya-wetlands-water-surface.git
   cd konya-wetlands-water-surface
   pixi install
   ```

   Linux (x86-64) only: the pixi lock file is solved for `linux-64`. On macOS or Windows use Docker. Pixi installs everything from `pixi.toml` and `pixi.lock` into `.pixi/`; `pixi run <task>` runs a
   task in that environment without activating it.

### Accounts each step needs

| What you run | Data | Account needed |
| --- | --- | --- |
| `pixi run snakemake --cores 1` (claims C1-C3) | Landsat Collection 2 (Microsoft Planetary Computer), JRC Global Surface Water, HydroBASINS, OpenStreetMap seed points | **none**: all public and anonymous |
| `pixi run snakemake --cores 1 climate` (basin water balance) | ERA5-Land monthly means | **Copernicus Climate Data Store** (free) |
| | Climate DT generation 2 monthly means, IFS-FESOM and IFS-NEMO, 1990-2049 | **DestinE upgraded access** |

Accounts are read from your home directory or the environment, never from the repository, and nothing in `work/`
(the downloads) is committed. Set up only the ones for the steps you run.

### Copernicus Climate Data Store (ERA5-Land)

1. Create a free account at <https://cds.climate.copernicus.eu> and log in.
2. Accept the licence of each dataset used, on the dataset page under *Download* → *Terms of use*: `reanalysis-era5-land-monthly-means`.
3. Copy your personal access token from your profile page into `~/.cdsapirc`:

   ```
   url: https://cds.climate.copernicus.eu/api
   key: <your personal access token>
   ```

   `cdsapi` also reads `CDSAPI_URL` and `CDSAPI_KEY` from the environment. Requests wait in the CDS queue (minutes to
   hours); the downloads are resumable.

### Destination Earth: Climate DT (DestinE upgraded access)

1. Create an account on the DestinE Platform, <https://platform.destine.eu/>, and request **upgraded access**, which
   includes the Climate Change Adaptation Digital Twin. Eligibility and terms are set by the platform (at the time of
   writing: users in EU Member States and in countries associated with the Digital Europe Programme; check the current
   terms of use before you apply). Upgraded access is not automatic: allow time for the request to be reviewed.
2. Get the Polytope key (an offline token) with ECMWF's script; it asks for your DestinE user name and password and
   writes `{"user_key": "<offline token>"}` to `~/.polytopeapirc`:

   ```bash
   curl -sO https://raw.githubusercontent.com/destination-earth-digital-twins/polytope-examples/main/desp-authentication.py
   pixi run python desp-authentication.py
   ```

   `polytope-client` also reads `POLYTOPE_USER_KEY` from the environment. A *DestinE Data Lake* (DEDL) API key is a
   different credential and is refused by Polytope (HTTP 401).
3. Authentication is not authorisation: a valid key can still be refused the data if upgraded access has not been
   granted yet; the first request tells you.
4. Terms: raw Climate DT data may not be redistributed. The pipeline keeps downloads in `work/` (not in git) and
   commits only derived statistics; keep it that way in any fork.

### Run

```bash
pixi run snakemake --cores 1             # claims C1-C3: no account; the Landsat step takes about 40 min and is resumable
pixi run snakemake --cores 1 climate     # basin water balance: CDS and DestinE accounts
```

Single steps: `pixi run aoi` (site outlines, JRC reference), `pixi run landsat` (every Landsat scene 1984-2025),
`pixi run analyse` (claims C1 and C3, figures), `pixi run python pipeline/03_basin_jrc.py work` (claim C2; downloads
HydroBASINS level 4 from data.hydrosheds.org itself).

Every step is a script in `pipeline/` with its usage in its docstring; `Snakefile` gives the order, inputs and
outputs. `pixi run snakemake --cores 1 --dry-run` lists what would run without downloading anything.
The charts of the LifeWatch country file are in `docs/country_file/` (chart code and the rows they plot).

### With Docker

The image holds the environment and the code, never an account. Put the accounts the steps need in a file that
stays on your machine (for example `~/credentials.env`, outside the repository) and pass it at run time, from the
cloned repository (so that `work/` and `results/` are kept on your disk):

```
CDSAPI_URL=https://cds.climate.copernicus.eu/api
CDSAPI_KEY=<CDS personal access token>
COPERNICUSMARINE_SERVICE_USERNAME=<Copernicus Marine user name>
COPERNICUSMARINE_SERVICE_PASSWORD=<Copernicus Marine password>
POLYTOPE_USER_KEY=<DestinE offline token>
```

```bash
docker run --rm --env-file ~/credentials.env -v "$PWD/work:/app/work" -v "$PWD/results:/app/results" \
    ghcr.io/annefou/konya-wetlands-water-surface:latest pixi run snakemake --cores 1 climate
```

Leave out the lines a step does not need. The image is published on GitHub's container registry with each release.

## Built from a template

This repository was created from [`sciencelivehub/forrt-replication-template`](https://github.com/sciencelivehub/forrt-replication-template). The template ships an operating manual for AI assistants ([`CLAUDE.md`](CLAUDE.md), [`AGENTS.md`](AGENTS.md)), domain conventions ([`DOMAIN.md`](DOMAIN.md)), and reference docs (`docs/`) so that an AI working only inside this repository can guide a researcher from "paper PDF + GitHub repo" to "published FORRT chain + Zenodo DOI" with no other context.

If you are reading this in a fresh fork, run [`/init-template`](.claude/skills/init-template/SKILL.md) inside Claude Code to substitute the placeholder tokens with your details. (For other AI tools, see [`docs/ai-portability.md`](docs/ai-portability.md).)

After `/init-template`, do these one-time setup steps to enable the full CI/CD path:

- **Enable GitHub Pages** at *Settings → Pages → Source: GitHub Actions*. Until enabled, the Jupyter Book build runs but the deploy step is skipped (CI stays green).
- All three workflows share one **readiness guard** (`.github/actions/check-ready`). Before `/init-template` runs, the `.template-uninitialised` sentinel makes them skip with an informative `::notice::` (badges stay green); `/init-template` deletes the sentinel, which activates them. They also skip while `notebooks/*.py` are still scaffolds (Phase 2). **Once you've published a nanopub chain** (real URIs in `nanopubs/PUBLISHED.md`), a skip is treated as a bug and **fails the run loudly** — so a finished replication can't sit on silently-green-but-empty CI.

## Repository structure

```
.
├── CLAUDE.md / AGENTS.md       # operating manual for AI assistants
├── DOMAIN.md                   # domain flavour (current: biodiversity + earth observation)
├── USER_PREFERENCES.md         # per-user style (edit on first clone)
├── README.md                   # this file
├── LICENSE                     # MIT
├── CITATION.cff                # how to cite
├── codemeta.json               # software metadata (CodeMeta-2.0)
├── ro-crate-metadata.json      # research object packaging (RO-Crate 1.2)
├── pixi.toml + pixi.lock       # pinned dependencies (single source of truth; lockfile is per-platform)
├── Dockerfile                  # container build
├── Snakefile                   # pipeline orchestration
├── myst.yml + index.md         # Jupyter Book scaffold
├── paper/                      # the source paper PDF
├── data/                       # downloaded artefacts (gitignored)
├── notebooks/                  # jupytext .py pipeline (01–04)
├── nanopubs/                   # FORRT chain drafts + published-URI registry
├── docs/                       # reference material
├── figures/                    # curated figures used in the Jupyter Book
├── .github/workflows/          # CI, Jupyter Book, Docker
└── .claude/                    # Claude Code agents, skills, sandbox config
```

## What you get

This template bakes in conventions that took multiple replications to discover. By using it, you inherit:

- **FAIR4RS conformance** — see [`docs/fair4rs-checklist.md`](docs/fair4rs-checklist.md) for the principle-by-principle mapping.
- **Self-contained data downloads** — the first notebook fetches everything; no manual data prep.
- **`pixi.toml` + `pixi.lock` as single source of truth** — local dev, Docker, and CI all install the same per-platform-pinned env.
- **`prefix-dev/setup-pixi`-based CI** — caches the env, runs the pipeline with `pixi run`, executes notebooks via a glob, fails fast on a stale lockfile.
- **Jupyter Book deployment** — auto-deploys to GitHub Pages with `BASE_URL` set correctly. (Don't put `base_url` in `myst.yml` — MyST silently ignores it.)
- **Docker + GHCR + Zenodo image archival** — `release` trigger pushes to GHCR and (optionally) archives to Zenodo for long-term preservation.
- **RO-Crate packaging** — the entire repo is a navigable Research Object via `ro-crate-metadata.json` (Process Run Crate + Workflow RO-Crate profiles).
- **Six-step FORRT chain workspace** — `nanopubs/drafts/` has a field-by-field skeleton for each step. `nanopubs/PUBLISHED.md` is the URI registry.
- **Layered AI guidance** — `CLAUDE.md` (universal) + `DOMAIN.md` (swappable per field) + `USER_PREFERENCES.md` (per-user). See [`docs/ai-portability.md`](docs/ai-portability.md) for non-Claude AI tools.
- **Sandbox by default** — `.claude/settings.json` denies file ops outside the repo, so a fresh AI session can't accidentally read `~/.ssh/` or write to `/etc/`.

## The six FORRT chain steps

A complete FORRT chain has six steps published on [platform.sciencelive4all.org](https://platform.sciencelive4all.org):

```
Quote-with-comment  →  AIDA  →  FORRT Claim  →  Replication Study  →  Replication Outcome  →  CiTO Citation
```

(For question-rooted chains with no upstream paper, replace step 1 with PICO or PCC. See [`docs/chain-decision-tree.md`](docs/chain-decision-tree.md).)

Drafts live in [`nanopubs/drafts/`](nanopubs/drafts/) field-by-field. Published URIs go into [`nanopubs/PUBLISHED.md`](nanopubs/PUBLISHED.md).

Optional further layers:

- **Research Software nanopub** — for reusable upstream tools (not demo repos). See [`docs/forrt-form-fields.md`](docs/forrt-form-fields.md) § Research Software.
- **Research Synthesis nanopub** — when this chain is part of a multi-chain story. See [`docs/forrt-form-fields.md`](docs/forrt-form-fields.md) § Research Synthesis.

## After publishing

When the chain is live and the FAIR4RS checklist is green, drafting an announcement post is the next step. See [`docs/announcement-template.md`](docs/announcement-template.md) for the structural template (vision-piece-first; the worked replication is the payoff, not the lead).

For lower-level nanopub work — retraction, superseding, batch publishing — see [`docs/programmatic-nanopubs.md`](docs/programmatic-nanopubs.md).

## Citation

If you use this work, please cite both:

- This software: [`CITATION.cff`](CITATION.cff) → DOI [10.5281/zenodo.23942467](https://doi.org/10.5281/zenodo.23942467)
- The original paper: [10.17501/iccc.2018.2102](https://doi.org/10.17501/iccc.2018.2102)

## Acknowledgements

This repository was built from [`sciencelivehub/forrt-replication-template`](https://github.com/sciencelivehub/forrt-replication-template), part of the [Science Live platform](https://platform.sciencelive4all.org). The template is licensed MIT and contributions (especially new domain flavours under [`docs/domain-flavours/`](docs/domain-flavours/)) are welcome.

# konya-wetlands-water-surface

[![CI](https://github.com/annefou/konya-wetlands-water-surface/actions/workflows/ci.yml/badge.svg)](https://github.com/annefou/konya-wetlands-water-surface/actions/workflows/ci.yml)
[![Jupyter Book](https://github.com/annefou/konya-wetlands-water-surface/actions/workflows/jupyter-book.yml/badge.svg)](https://annefou.github.io/konya-wetlands-water-surface/)
[![Docker](https://github.com/annefou/konya-wetlands-water-surface/actions/workflows/docker.yml/badge.svg)](https://github.com/annefou/konya-wetlands-water-surface/pkgs/container/konya-wetlands-water-surface)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/{{ZENODO_DOI}}.svg)]({{ZENODO_DOI}})
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

- **C1 reproduced for 1987, 2007 and 2017**: the scene closest to the paper's value is 2999 ha on 9 June 1987 (paper 2958.4), 19.3 ha on 15 May 2007 (12.7), 128.7 ha on 11 June 2017 (117.2). For 1998 our valid scenes peak at 731 ha (1087 ha at NDWI > -0.1), below the paper's 1153.9 ha. One image per year hides a two-fold seasonal range: 3,939 ha on 22 April and 1,920 ha on 27 July 1987.
- **C2 consistent**: JRC water 2,540 km2 (1984) -> 2,033 km2 (2021), **-20.0 %**; without Tuz Gölü, **-40.4 %** (1,477 -> 880 km2). Tuz Gölü, a shallow salt lake holding 40 % of the basin's water, hides the loss of the freshwater lakes and wetlands.
- **C3 supported, in a stronger form** (a year counts as filled when its spring maximum reaches half the 1984-1995 median spring maximum): Akgöl filled in every year of the 1980s, 40 % of the 1990s, never since 2000 (spring maximum 3,436 -> 282 ha, 1984-95 vs 2015-25 medians); Hotamış 1,217 -> 25 ha, never since 2010; Meke (Ramsar) 53 -> 2 ha, never in the 2020s; Meyil 6.7 -> 1.7 ha, 78 % of the 2010s and never in the 2020s. The crater lake Acıgöl (Karapınar) is stable (109 -> 97 ha) and serves as a control. Table: `results/fill_by_decade.csv`.
- **NDWI caveat**: NDWI misses bright or turbid water in some scenes (Acıgöl reads 0 ha from January to June 1996; Meyil reads 0 in some scenes); the reference is therefore the median of yearly spring maxima, not of single scenes. MNDWI (SWIR) would be more robust for the crater lakes; the replication keeps the paper's NDWI.

Figures: [Akgöl, every scene](figures/akgol_scenes.png) · [spring and summer per site](figures/sites_spring_summer.png) · [drying date](figures/sites_drying_doy.png). Tables: `results/`.

### Method

- Landsat Collection 2 Level-2 (Landsat 5, 7, 8, 9) from Microsoft Planetary Computer, anonymous access. Each scene: green, NIR and QA_PIXEL read for the site window; cloud, shadow, snow and fill masked; green and NIR resampled onto HEALPix cells (depth 17, ~49 m, [healpix-geo](https://github.com/GRID4EARTH/healpix-geo) on the WGS84 ellipsoid, NESTED) with [healpix-resample](https://github.com/GRID4EARTH/healpix-resample) (conservative bilinear) **before** NDWI and its threshold (NDWI > 0; -0.1 and +0.1 as sensitivity). A scene counts for a site when at least 95 % of its cells are valid.
- Site outlines: JRC Global Surface Water v1.4 maximum extent around seed points checked on OpenStreetMap.
- Basin: HydroBASINS level 4, endorheic basin 2040085960 (58,374 km2).

### Basin water balance: climate or water use?

`pipeline/04a_era5land_monthly.py` (ERA5-Land monthly means, CDS), `pipeline/04b_climatedt_monthly.py` (Climate DT generation 2 monthly means, IFS-FESOM and IFS-NEMO, 1990-2049, region cut out by Polytope, sphere -> WGS84 with healpix-connector) and `pipeline/04c_water_balance.py` compute the natural water balance of HydroBASINS 2040085960 on 1,442 depth-10 cells (`pipeline/basin.py`). Water years 1991-2025: precipitation -10% (not significant), summer temperature +0.49 degC and potential evaporation +33 mm per decade; in the wettest third of years the four collapsed wetlands filled to 67% (1991-2005) and 23% (2011-2025) of their 1984-1995 level. Climate DT 2040s: precipitation -14 to -16%, summers +2.3 to +2.9 degC. ERA5-Land has no irrigation; groundwater and irrigated-area data would test the water-use explanation. Results: `results/water_balance_claims.json`; only basin means are committed (DestinE terms).

### Limits

- The paper's image dates are not stated; we compare with the range of all valid scenes in each year.
- 2012-2013 has no valid scenes (end of Landsat 5, before Landsat 8; Landsat 7 scan-line gaps fail the 95 % rule). Two 2022 scenes could not be read and are excluded.
- NDWI on salt crust and on shallow turbid water is uncertain; Tuz Gölü is separated with a 0.45 deg circle.
- Water surface only: no depth, salinity or ecological condition.

### Data

Landsat (USGS, public domain), JRC Global Surface Water (CC BY 4.0), HydroBASINS (CC BY 4.0), OpenStreetMap (ODbL, seed points only). Only code, plots and summary statistics are in this repository; inputs are fetched by the pipeline.

---

## Quick start

```bash
git clone https://github.com/annefou/konya-wetlands-water-surface.git
cd konya-wetlands-water-surface
pixi install
pixi run aoi                  # site outlines and JRC reference (results/sites_jrc.json)
pixi run landsat              # every Landsat scene 1984-2025 (resumable, about 40 min)
pixi run analyse              # claims C1 and C3, figures
pixi run python pipeline/03_basin_jrc.py work     # claim C2 (needs work/basin/hybas_eu_lev04.zip from data.hydrosheds.org)
```

(Pixi resolves `pixi.toml` against the per-platform `pixi.lock`, installs the env under `.pixi/`, and provides `pixi run` for any task without needing an `activate` step.)

Or with Docker:

```bash
docker run --rm ghcr.io/annefou/konya-wetlands-water-surface:latest
```

The Jupyter Book version is at <https://annefou.github.io/konya-wetlands-water-surface/>.

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

- This software: [`CITATION.cff`](CITATION.cff) → DOI [{{ZENODO_DOI}}]({{ZENODO_DOI}})
- The original paper: [10.17501/iccc.2018.2102](https://doi.org/10.17501/iccc.2018.2102)

## Acknowledgements

This repository was built from [`sciencelivehub/forrt-replication-template`](https://github.com/sciencelivehub/forrt-replication-template), part of the [Science Live platform](https://platform.sciencelive4all.org). The template is licensed MIT and contributions (especially new domain flavours under [`docs/domain-flavours/`](docs/domain-flavours/)) are welcome.

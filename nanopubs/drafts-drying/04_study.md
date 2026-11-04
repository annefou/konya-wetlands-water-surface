# 04 — FORRT Replication Study

Method read from `pipeline/00_aoi.py`, `pipeline/01_landsat_scenes.py` and `pipeline/02_analyse.py` (2026-10-24).

## Field-by-field draft

<!-- field: study -->
### Short URI suffix for study ID (text input, required)

```
konya-wetlands-earlier-drying-replication-study
```

<!-- field: label -->
### Label/name of replication study (text input, required)

```
Replication of the earlier drying of Konya Closed Basin wetlands with every valid Landsat scene, 1984-2025
```

<!-- field: type -->
### Choose the study type (dropdown, required)

Same sensors (reproduction of the data source) but a different index, other sites, every scene and a drying-date metric (replication).

- [x] Replication Study - replication with different methodology or conditions
- [ ] Reproduction/Replication Study - study that is both, reproduction and replication
- [ ] Reproduction Study - direct reproduction: same methodology, same tools

<!-- field: claim -->
### Choose FORRT claim (search/select, required)

```
«URI of step 03 (FORRT Claim), filled by the chain wizard»
```

<!-- field: scope -->
### Describe what part of the claim is reproduced/replicated. (textarea, required)

```
The claim that wetlands of the Konya Closed Basin shrink and dry earlier in the breeding season in the late 2010s than in the late 1990s. In scope: the date each year at which a wetland falls to a small fraction of its spring area, compared between 1996-2000 and 2016-2020 and as a trend over 1984-2025, and whether the wetlands still fill in spring at all. Out of scope: the bird diversity results, the causes of the change, and the paper's seven lakes as such (only some of the sites overlap).
```

<!-- field: methodology -->
### Describe how the claim is reproduced/replicated. (textarea, required)

```
Every valid Landsat Collection 2 Level-2 scene (Landsat 4, 5, 7, 8 and 9) from 1984 to 2025 at six sites: Akgöl, Hotamış, Meke (Ramsar), Meyil, Bolluk and the crater lake Acıgöl (Karapınar) as a stable control. Site outlines from the JRC Global Surface Water maximum extent; green and near-infrared resampled onto HEALPix cells of about 25 m (depth 18, WGS84 ellipsoid, nested) before NDWI > 0; scenes kept with at least 95% valid cells. Reference area per site: median over 1984-1995 of each year's spring (March-June) maximum. Drying date: first valid scene after day 100 with water at most 10% of the reference; years that never fall that low are censored at day 366. Compared as medians of 1996-2000 against 2016-2020, as the paper's windows, and as a Theil-Sen trend over all years. Filling: share of years per decade whose spring maximum reaches half the reference.
```

<!-- field: deviation -->
### Describe any deviations from original methodology. (textarea, optional)

```
The paper used seven Important Bird Area lakes, a few images per year in early (April-May) and late (July-August) breeding season, Level-1 products corrected in QGIS and MNDWI. This study uses six sites that only partly overlap, every valid scene, Collection 2 surface reflectance, NDWI, and a drying date rather than the mean area in two parts of the season, and extends the record to 1984-2025.
```

<!-- field: keyword -->
### Search keywords (Wikidata) (search/select, optional)

Checked with `wikidata_lookup` (2026-10-24).

- wetland (Q170321)
- remote sensing (Q199687)

<!-- field: discipline -->
### Search discipline (Wikidata) (search/select, optional)

- hydrology (Q42250)

## Publication note

After publishing, paste the resulting URI into `nanopubs/drafts-drying/PUBLISHED.md` step 04.

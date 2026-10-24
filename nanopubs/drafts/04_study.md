# 04 — FORRT Replication Study

Method read from `pipeline/00_aoi.py`, `pipeline/01_landsat_scenes.py`, `pipeline/02_analyse.py` and `pipeline/03_basin_jrc.py` (2026-10-24).

## Field-by-field draft

<!-- field: study -->
### Short URI suffix for study ID (text input, required)

```
akgol-water-surface-replication-study
```

<!-- field: label -->
### Label/name of replication study (text input, required)

```
Replication of the Akgöl water-surface loss with every valid Landsat scene 1984-2025 on HEALPix cells
```

<!-- field: type -->
### Choose the study type (dropdown, required)

Same sensors and index (reproduction); every scene instead of one per year, a fixed threshold and a different grid (replication).

- [ ] Replication Study - replication with different methodology or conditions
- [x] Reproduction/Replication Study - study that is both, reproduction and replication
- [ ] Reproduction Study - direct reproduction: same methodology, same tools

<!-- field: claim -->
### Choose FORRT claim (search/select, required)

```
«URI of step 03 (FORRT Claim), filled by the chain wizard»
```

<!-- field: scope -->
### Describe what part of the claim is reproduced/replicated. (textarea, required)

```
The claim that Akgöl wetland lost about 96% of its water surface between 1987 and 2017 (2958.4 ha to 117.2 ha). In scope: the four yearly areas the paper reports (1987, 1998, 2007, 2017), the size of the loss when all valid scenes of each year are used, whether the loss persists through 2025, and, as context, the paper's basin-wide decline of about 23.5%. Out of scope: the GIS layers on settlements and infrastructure, and the paper's statement that the decrease matches the meteorological conditions (tested separately).
```

<!-- field: methodology -->
### Describe how the claim is reproduced/replicated. (textarea, required)

```
All Landsat Collection 2 Level-2 scenes (Landsat 4, 5, 7, 8 and 9) over Akgöl from 1984 to 2025, read from Microsoft Planetary Computer. For each scene the green and near-infrared bands are read for the site window, cloud, shadow, snow and fill pixels are masked with QA_PIXEL, and the bands are resampled onto HEALPix cells of about 49 m (depth 17, WGS84 ellipsoid, nested) with conservative bilinear resampling before computing NDWI as in the paper. Water is NDWI above 0, with -0.1 and +0.1 as sensitivity. A scene counts when at least 95% of the site's cells are valid (455 scenes). The site outline is the JRC Global Surface Water maximum extent. For each of the paper's years the scene closest to its value and the range over all scenes are reported; for the long-term change, the median over 1984-1995 and over 2015-2025 of each year's spring (March-June) maximum. The basin figure uses JRC Global Surface Water transitions 1984-2021 over HydroBASINS basin 2040085960.
```

<!-- field: deviation -->
### Describe any deviations from original methodology. (textarea, optional)

```
Every valid scene instead of one hand-picked image per year; a fixed NDWI threshold with sensitivity instead of a threshold chosen per image; Collection 2 surface reflectance instead of the images processed in ERDAS; HEALPix cells of about 49 m instead of 30 m pixels; the record extended to 2025. The basin-wide figure uses JRC Global Surface Water (1984-2021) over the HydroBASINS endorheic basin instead of the paper's 16 water bodies.
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

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.

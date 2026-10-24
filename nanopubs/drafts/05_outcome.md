# 05 — FORRT Replication Outcome

Numbers read from `results/claims.json`, `results/akgol_paper_years.csv`, `results/fill_by_decade.csv` and `results/basin_jrc.json` (2026-10-24).

## Field-by-field draft

<!-- field: outcome -->
### Short URI suffix for outcome ID (text input, required)

```
akgol-water-surface-loss-outcome
```

<!-- field: label -->
### Plain-text label for the outcome (text input, required)

```
Akgöl's loss of open water reproduced with every Landsat scene 1984-2025; it has not refilled since 2000
```

<!-- field: study -->
### Choose study (search/select, required)

```
«URI of step 04 (FORRT Replication Study), filled by the chain wizard»
```

<!-- field: repo -->
### Repository URL (text input, required)

The Zenodo version DOI of the release the results come from; substituted by the release workflow.

```
https://doi.org/{{ZENODO_VERSION_DOI}}
```

<!-- field: date -->
### Choose completion date (text input, required)

```
2026-10-23
```

<!-- field: validationStatus -->
### Choose validation status (dropdown, required)

From `vocabulary("validation_status")`: the size of the 1987-2017 loss is reproduced and holds with every scene and through 2025; only the 1998 intermediate value is not.

- [ ] contradicted
- [ ] inconclusive
- [ ] not tested
- [ ] partially supported
- [x] validated

<!-- field: confidenceLevel -->
### Choose confidence level (dropdown, required)

From `vocabulary("confidence_level")`: three of the four yearly values reproduced, and the loss is robust to scene choice and threshold.

- [x] high - Strong evidence, mostly agrees with original
- [ ] low - Limited evidence, significant disagreement
- [ ] moderate - Adequate evidence, partial agreement
- [ ] very high - Extensive evidence, high agreement with original
- [ ] very low - Minimal evidence, major disagreement

<!-- field: conclusion -->
### Describe the overall conclusion about the original claim (textarea, required)

```
The paper's loss of open water at Akgöl is reproduced. Scenes close to the paper's values exist for 1987 (2999 ha against 2958.4), 2007 (19.3 against 12.7) and 2017 (128.7 against 117.2), a loss of 95.7% from 1987 to 2017 against the paper's 96%. Using every valid scene, the median spring maximum fell from 3436 ha in 1984-1995 to 282 ha in 2015-2025, a loss of 92%, and Akgöl has not filled to half its 1984-1995 level in any year since 2000. Only the paper's 1998 value (1153.9 ha) is not matched: our valid 1998 scenes peak at 731 ha. Single images per year hide a two-fold seasonal range (3939 ha in April and 1920 ha in July 1987), but not the loss.
```

<!-- field: evidence -->
### Describe the evidence that supports your conclusion (textarea, required)

```
455 valid Landsat scenes of Akgöl, 1984-2025, NDWI > 0 on HEALPix depth 17. Paper years, paper value / closest scene / range over scenes (ha): 1987 2958.4 / 2999.4 (9 June) / 1920-3939, 3 scenes; 1998 1153.9 / 730.9 (7 June) / 45-731, 6 scenes; 2007 12.7 / 19.3 (15 May) / 0-19, 8 scenes; 2017 117.2 / 128.7 (11 June) / 0-421, 13 scenes. Threshold sensitivity at the closest scene, NDWI -0.1 to +0.1: 1987 2536-3505 ha; 2017 104-170 ha. Median spring maximum 1984-1995 3436 ha, 2015-2025 282 ha. Years filled to half the 1984-1995 level: 100% of the 1980s, 40% of the 1990s, none since 2000. Basin, JRC Global Surface Water 1984-2021: -20.0% (paper about -23.5%), -40.4% without Tuz Gölü. Files: results/claims.json, results/fill_by_decade.csv, results/basin_jrc.json.
```

<!-- field: limitations -->
### Describe what limits the conclusions of the study (textarea, optional)

```
NDWI misses bright or turbid water in some scenes, so single scenes can read too low; the long-term figure uses yearly spring maxima for that reason. The paper's 1998 image and its per-image thresholds are unknown, which may explain the 1998 gap. Landsat 7 scenes after 2003 whose scan-line gaps cross the site fail the 95% valid-cell rule and are dropped. The basin comparison uses a different water product and basin outline from the paper. The causes of the loss (dams, drainage, irrigation, climate) are not tested here.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.

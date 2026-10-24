# 05 — FORRT Replication Outcome

Numbers read from `results/water_balance_claims.json` (2026-10-24).

## Field-by-field draft

<!-- field: outcome -->
### Short URI suffix for outcome ID (text input, required)

```
konya-wetland-decline-meteorology-outcome
```

<!-- field: label -->
### Plain-text label for the outcome (text input, required)

```
Rainfall does not explain the Konya wetland collapse: wet years no longer refill them; warming adds evaporative demand
```

<!-- field: study -->
### Choose study (search/select, required)

```
«URI of step 04 (FORRT Replication Study), filled by the chain wizard»
```

<!-- field: repo -->
### Repository URL (text input, required)

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

From `vocabulary("validation_status")`: the temperature side of the claim holds, the precipitation side does not.

- [ ] contradicted
- [ ] inconclusive
- [ ] not tested
- [x] partially supported
- [ ] validated

<!-- field: confidenceLevel -->
### Choose confidence level (dropdown, required)

From `vocabulary("confidence_level")`: a clear wet-year contrast, but no data on irrigation or groundwater, and five wet years per period.

- [ ] high - Strong evidence, mostly agrees with original
- [ ] low - Limited evidence, significant disagreement
- [x] moderate - Adequate evidence, partial agreement
- [ ] very high - Extensive evidence, high agreement with original
- [ ] very low - Minimal evidence, major disagreement

<!-- field: conclusion -->
### Describe the overall conclusion about the original claim (textarea, required)

```
The weather alone does not account for the decline. Over the Konya Closed Basin, precipitation in water years 1991-2025 changed by -14 mm per decade (95% interval -36 to +8), not a significant trend, and the last decade was 10% drier than the 1990s. In the wettest years, with similar rainfall in both periods (446-555 mm in 1991-2005, 436-534 mm in 2011-2025), the four collapsed wetlands filled in spring to 67% of their 1984-1995 level before and to 23% after. Summer temperature rose by 0.49 degC per decade and potential evaporation by 33 mm per decade, both significant, so warming adds demand. The decline is consistent with warming and with rising water use, not with a fall in rainfall.
```

<!-- field: evidence -->
### Describe the evidence that supports your conclusion (textarea, required)

```
ERA5-Land basin means over 1,442 HEALPix cells, water years 1991-2025, Theil-Sen per decade (95% interval): precipitation -14.4 mm (-36.3 to 7.9), mean 421 mm in 1991-2020; evaporation -3.9 mm (-17.3 to 5.7); P - E -6.2 mm (-18.3 to 7.0); potential evaporation +32.8 mm (1.3 to 66.4); June-August temperature +0.49 degC (0.17 to 0.77). 2016-2025 against 1991-2000: precipitation -10.0%, summer temperature +1.3 degC. Wet-year spring fill of Akgöl, Hotamış, Meke and Meyil: 67.4% (1995, 1996, 1997, 1999, 2002) against 22.6% (2011, 2015, 2017, 2019, 2022). Climate DT 2040s against 1991-2020: precipitation -16.3% (IFS-FESOM) and -14.3% (IFS-NEMO), summer temperature +2.85 and +2.34 degC. File: results/water_balance_claims.json.
```

<!-- field: limitations -->
### Describe what limits the conclusions of the study (textarea, optional)

```
The record starts in 1991, after much of the decline at Akgöl (1987-1998); the paper's stations cover 1971-2015. ERA5-Land has no irrigation, groundwater abstraction or dams, so water use is inferred from what climate fails to explain, not measured; groundwater and irrigated-area data from DSİ would test it. Five wet years per period. Reanalysis precipitation over a semi-arid basin carries its own uncertainty, and Climate DT has biases against ERA5-Land (precipitation -19% for IFS-FESOM), so only its changes are used.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/drafts-climate/PUBLISHED.md` step 05.

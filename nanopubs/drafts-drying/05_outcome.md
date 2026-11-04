# 05 — FORRT Replication Outcome

Numbers read from `results/claims.json` (`C2_drying`) and `results/fill_by_decade.csv` (2026-10-24).

## Field-by-field draft

<!-- field: outcome -->
### Short URI suffix for outcome ID (text input, required)

```
konya-wetlands-earlier-drying-outcome
```

<!-- field: label -->
### Plain-text label for the outcome (text input, required)

```
Konya wetlands dry earlier over 1984-2025 at three of five sites; the larger change is that they no longer fill
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

From `vocabulary("validation_status")`: the long-term advance holds at three sites, but not between the paper's two windows.

- [ ] contradicted
- [ ] inconclusive
- [ ] not tested
- [x] partially supported
- [ ] validated

<!-- field: confidenceLevel -->
### Choose confidence level (dropdown, required)

From `vocabulary("confidence_level")`: different sites, index and metric from the paper.

- [ ] high - Strong evidence, mostly agrees with original
- [ ] low - Limited evidence, significant disagreement
- [x] moderate - Adequate evidence, partial agreement
- [ ] very high - Extensive evidence, high agreement with original
- [ ] very low - Minimal evidence, major disagreement

<!-- field: conclusion -->
### Describe the overall conclusion about the original claim (textarea, required)

```
Over 1984-2025 the drying date advanced at Akgöl (44 days per decade), Hotamış (24) and Meke (58), all significant; Meyil and Bolluk show no trend and the control crater lake never dries. Between the paper's windows the median drying date advanced only at Akgöl (day 185 to 165), not at Hotamış (121 to 119), Meke (145 to 165) or Meyil (107 to 139). The reason is a larger change: the wetlands stopped filling. Akgöl filled to half its 1984-1995 spring level in every year of the 1980s, 40% of the 1990s and never since 2000; Hotamış never since 2010; Meke and Meyil in no year of the 2020s. Earlier drying is supported as a long-term trend; the dominant signal is the failure to fill.
```

<!-- field: evidence -->
### Describe the evidence that supports your conclusion (textarea, required)

```
Drying date (first scene after day 100 with water at most 10% of the 1984-1995 spring reference), Theil-Sen days per decade over 1984-2025 (95% interval): Akgöl -44.2 (-69.3 to -23.6), Hotamış -23.5 (-45.2 to -8.6), Meke -58.3 (-77.3 to -9.1), Meyil 1.0 (-6.7 to 14.1), Bolluk 0.0 (-35.9 to 30.0), Acıgöl control 0.0 (never dry). Median day of year 1996-2000 against 2016-2020: Akgöl 185/165, Hotamış 121/119, Meke 145/165, Meyil 107/139, Bolluk 149.5/366, Acıgöl 145/366. HEALPix depth 18 (about 25 m). Share of years filled to half the reference, 1980s/1990s/2000s/2010s/2020s: Akgöl 1.0/0.4/0/0/0; Hotamış 1.0/0.3/0.3/0/0; Meke 1.0/1.0/1.0/0.44/0; Meyil 1.0/1.0/1.0/0.78/0; Acıgöl 1.0/0.9/1.0/1.0/1.0. Files: results/claims.json, results/fill_by_decade.csv.
```

<!-- field: limitations -->
### Describe what limits the conclusions of the study (textarea, optional)

```
The paper's seven lakes are listed in its supplement, which was not used; only some sites overlap. NDWI rather than the paper's MNDWI: it misses bright or turbid water in some scenes, notably at the crater lakes, which can set drying dates too early. A drying date is undefined in a year when a wetland does not fill, so collapse and earlier drying are hard to separate; the fill share is reported for that reason. Bolluk has few early years. No breeding-season bird data were analysed.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/drafts-drying/PUBLISHED.md` step 05.

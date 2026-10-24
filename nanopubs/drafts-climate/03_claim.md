# 03 — FORRT Claim

## Field-by-field draft

<!-- field: claim -->
### Short URI suffix as claim ID (text input, required)

```
konya-wetland-decline-meteorology-claim
```

<!-- field: label -->
### Label of the claim, to find it later (text input, required)

```
Decrease of Akgöl's water surface matched with the meteorological conditions (Musaoğlu et al. 2018)
```

<!-- field: aida -->
### Search for an AIDA sentence (search/select, required)

```
«URI of step 02 (AIDA), filled by the chain wizard»
```

<!-- field: forrtType -->
### Type of FORRT claim (dropdown, required)

From `vocabulary("claim_type")` (live, 2026-10-24): a correspondence between two time series, stated without a test, so a descriptive pattern.

- [ ] computational performance (Computational & Performance)
- [ ] data governance (access control, licensing, FAIR compliance)
- [ ] data quality (preprocessing, validation, normalization)
- [x] descriptive pattern (distribution, trend, proportion)
- [ ] model performance (accuracy, F1 score, evaluation metrics)
- [ ] scalability (Computational & Performance)
- [ ] statistical significance (significant difference, relationship, or effect)

<!-- field: source -->
### Source URI (text input, optional)

```
https://doi.org/10.17501/iccc.2018.2102
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/drafts-climate/PUBLISHED.md` step 03.

# 03 — FORRT Claim

**Form heading:** *"FORRT Claim — Declare an original claim according to FORRT, linking it to an AIDA sentence with a specific FORRT type."*

## Field-by-field draft

<!-- field: claim -->
### Short URI suffix as claim ID (text input, required)

```
akgol-water-surface-loss-claim
```

<!-- field: label -->
### Label of the claim, to find it later (text input, required)

```
Akgöl wetland lost about 96% of its water surface 1987-2017, Konya Closed Basin (Musaoğlu et al. 2018)
```

<!-- field: aida -->
### Search for an AIDA sentence (search/select, required)

```
«URI of step 02 (AIDA), filled by the chain wizard»
```

<!-- field: forrtType -->
### Type of FORRT claim (dropdown, required)

From `vocabulary("claim_type")` (live, 2026-10-24): a change over time in an area, so a descriptive pattern (trend).

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

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 03.

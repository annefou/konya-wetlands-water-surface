# 03 — FORRT Claim

## Field-by-field draft

<!-- field: claim -->
### Short URI suffix as claim ID (text input, required)

```
konya-wetlands-earlier-drying-claim
```

<!-- field: label -->
### Label of the claim, to find it later (text input, required)

```
Konya Closed Basin wetlands shrink and dry earlier in the breeding season, late 2010s against late 1990s (Özgencil et al. 2025)
```

<!-- field: aida -->
### Search for an AIDA sentence (search/select, required)

```
«URI of step 02 (AIDA), filled by the chain wizard»
```

<!-- field: forrtType -->
### Type of FORRT claim (dropdown, required)

From `vocabulary("claim_type")` (live, 2026-10-24): a change in seasonal timing, so a descriptive pattern (trend).

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
https://doi.org/10.1080/20442041.2025.2488655
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/drafts-drying/PUBLISHED.md` step 03.

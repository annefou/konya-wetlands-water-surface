# 01 — Quote-with-comment (paper-rooted chains)

Third chain of this repository: Özgencil et al. 2025, earlier drying of the wetlands. Built with `pixi run build-chain-draft-drying`; the paper DOI is drafted here and overrides `CITATION.cff`'s first article.

## Field-by-field draft

<!-- field: paper -->
### Cited DOI (text input, required)

Resolved with `resolve_doi` (2026-10-24): Özgencil et al. 2025, *Inland Waters* 15(1), 2488655.

```
10.1080/20442041.2025.2488655
```

### Quote mode (radio button)

- [x] **Quote whole text (less than 500 characters)**
- [ ] Quote start/end *(use this if the quote exceeds 500 chars)*

<!-- field: quotation -->
### The exact quotation from the paper (max. 500 characters) (textarea, required)

Verified with `verify_quote` on `paper/ozgencil-2025.pdf`: page 11, characters 860–1054, match "normalized".

```
We found that the wetlands in the basin were shrinking and drying earlier in the breeding season in the late 2010s than in the late 1990s, as demonstrated elsewhere (e.g., Rashford et al. 2016).
```

Character count: 194 / 500.

<!-- field: quotation-end -->
### End of quotation (optional - use when quoting beginning and end of a longer passage, max. 500 characters) (textarea, optional)

*(skip — single short quote)*

```

```

<!-- field: comment -->
### Our interpretation and explanation of why this quotation is relevant (max. 800 characters) (textarea, required)

```
The paper links the loss of late-breeding diving ducks in the Konya Closed Basin to wetlands that shrink and dry earlier in the season, based on Landsat images of seven lakes in 1996-1998 and 2016-2018. The timing matters because a wetland that dries in mid-season can make a whole breeding season fail. The replication tests the shift in drying date with every valid Landsat scene from 1984 to 2025 at five wetlands of the basin and a stable crater lake as control.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/drafts-drying/PUBLISHED.md` step 01.

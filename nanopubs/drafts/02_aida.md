# 02 — AIDA Sentence

**Form heading:** *"AIDA Sentence — Make structured scientific claims following the AIDA model"*

## Field-by-field draft

<!-- field: aida -->
### AIDA sentence (text input, required)

Atomic (one finding), no numbers, no method names.

```
Akgöl wetland in the Konya Closed Basin has lost almost all of its open water since the late 1980s.
```

<!-- field: topic -->
### Select related topics/tags (search/select, optional)

Checked with `wikidata_lookup` (2026-10-24). No Wikidata item matches the Akgöl of Ereğli (the only "Akgöl, lake in Turkey" item lies in Van province, not in Konya), so none is used.

```
wetland (Q170321)
remote sensing (Q199687)
```

<!-- field: project -->
### Relates to this nanopublication (search/select, required)

```
«URI of step 01 (Quote-with-comment), filled by the chain wizard»
```

<!-- field: dataset -->
### Supported by datasets (text input, optional)

Landsat Collection 2 Level-2, USGS EROS; DOIs resolved 2026-10-24.

- _DOI 1: https://doi.org/10.5066/P9IAXOVV
- _DOI 2: https://doi.org/10.5066/P9C7I13B
- _DOI 3: https://doi.org/10.5066/P9OGBGM6

<!-- field: publication -->
### Supported by other publications (text input, optional)

*(skip — the paper is cited through the Quote; leaving this empty also avoids the dataset + publication publish bug)*

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 02.

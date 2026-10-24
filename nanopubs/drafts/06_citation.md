# 06 — CiTO Citation

**Description:** *"Declare citations between papers or other works, using Citation Typing Ontology"*

## Field-by-field draft

<!-- field: work -->
### Identifier for the citing creative work (text input, required)

```
«URI of step 05 (FORRT Replication Outcome), filled by the chain wizard»
```

### List citations (repeatable group, required ≥1)

#### Citation 1 — back to the original paper

##### Citation Type (dropdown)

Outcome is "validated", so `confirms` (from `vocabulary("cito_relation")`, live).

```
confirms
```

##### DOI or other URL of the cited work (text input)

```
https://doi.org/10.17501/iccc.2018.2102
```

#### Additional citations (optional)

All DOIs resolved on 2026-10-24; relations from `vocabulary("cito_relation")`.

- Type: uses method in → URL: https://doi.org/10.1080/01431169608948714
- Type: cites as data source → URL: https://doi.org/10.5066/P9IAXOVV
- Type: cites as data source → URL: https://doi.org/10.5066/P9C7I13B
- Type: cites as data source → URL: https://doi.org/10.5066/P9OGBGM6
- Type: cites as data source → URL: https://doi.org/10.1038/nature20584

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 06.

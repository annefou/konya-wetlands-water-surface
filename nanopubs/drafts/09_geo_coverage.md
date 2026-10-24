# 09 — Geographical coverage (optional)

One coverage: the Konya Closed Basin, which contains Akgöl.

## Shared field

<!-- field: paper -->
### Cited DOI (text input, required — same for every location)

```
10.17501/iccc.2018.2102
```

---

## Per-location block

### Location A

<!-- field: quoteType -->
**Quote type** (radio: whole | ends, required)

```
whole
```

<!-- field: quotation -->
**Quoted Text** (textarea, required) — verified with `verify_quote` on `paper/musaoglu-2018.pdf`: page 2, characters 2458–2574, match "normalized".

```
Konya Closed Basin (KCB) located in Central Anatolia is one of the 25 river basins of Turkey and houses 13 wetlands.
```

<!-- field: quotation-end -->
**Quoted Text End** (textarea, optional — only if quote type = ends). Leave blank for `whole`.

```

```

<!-- field: location -->
**Short ID for location** (text input, required)

```
konya-closed-basin
```

<!-- field: location-label -->
**Area name** (text input, required) — search "Konya" in the form's location search and pick the basin or province area.

```
Konya Closed Basin, Central Anatolia, Türkiye
```

<!-- field: geometry -->
**Short ID for geometry** (text input, optional)

```
coverage
```

<!-- field: wkt -->
**Geometry as Well-known Text (WKT)** — left to the form's geocoder.

```

```

<!-- field: comment -->
**Comment** (textarea, required)

```
The quoted sentence names the study area: the endorheic Konya Closed Basin in Central Anatolia, which contains Akgöl wetland near Ereğli, the focus of the paper's headline result.
```

## Publication note

Each location block is a **standalone** nanopub, not one of the six FORRT chain steps.
Publish it via the platform's **"Document geographical coverage"** template. After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` under a "Geographical coverage" row.

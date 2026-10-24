# 09 — Geographical coverage (optional)

One coverage: the Konya Closed Basin, as in the paper.

## Shared field

<!-- field: paper -->
### Cited DOI (text input, required — same for every location)

```
10.1080/20442041.2025.2488655
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
**Quoted Text** (textarea, required) — verified with `verify_quote` on `paper/ozgencil-2025.pdf`: page 4, characters 32–94, match "normalized".

```
The current study focused on KCB in Central Anatolia, Türkiye.
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
The quoted sentence names the study area: the Konya Closed Basin (KCB), the largest endorheic basin of Türkiye, where the paper compares breeding bird atlases of 1998 and 2018 and the seasonal shrinking of seven Important Bird Area lakes.
```

## Publication note

Each location block is a **standalone** nanopub, not one of the six FORRT chain steps.
Publish it via the platform's **"Document geographical coverage"** template. After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` under a "Geographical coverage" row.

# 08 — Research Synthesis

**Form heading:** *"Science Live Research Synthesis — Synthesise findings across multiple replication outcomes with conclusions, recommendations, conditions, and limitations."*

Ties the three chains of this repository: the main chain (Akgöl's loss, `nanopubs/drafts/`), "climate" (`nanopubs/drafts-climate/`) and "drying" (`nanopubs/drafts-drying/`). It belongs to the chain published **last**, "drying": publish the main chain, then "climate", paste their Outcome URIs below, rebuild with `pixi run build-chain-draft-drying`, and publish "drying". The wizard appends the "drying" Outcome to the sources itself. Template fields checked with `template_fields("08_synthesis")` (live, 2026-10-24).

## Field-by-field draft

<!-- field: synthesis -->
### Short URI suffix for synthesis ID (text input, required)

```
konya-closed-basin-wetland-collapse-synthesis
```

<!-- field: label -->
### Label (text input, required)

```
Konya Closed Basin wetlands have stopped filling since the 1990s, more than the change in rainfall explains
```

<!-- field: conclusion -->
### Conclusion of the synthesis (textarea, required)

```
Three replications on every valid Landsat scene of 1984-2025 and an ERA5-Land water balance of the basin agree on one picture. Akgöl's loss of open water reported for 1987-2017 is reproduced (about 96% between the paper's dates, 92% between the median spring maxima of 1984-1995 and 2015-2025). The weather alone does not explain it: rainfall over 1991-2025 shows no significant trend, and in years as wet as before the four collapsed wetlands now fill to about a third of their former level (23% against 67%), while summers warmed and evaporative demand rose. Earlier drying in the season is seen as a long-term trend at three of five wetlands, but the dominant change is that the wetlands no longer fill at all: Akgöl not since 2000, Hotamış not since 2010, Meke and Meyil not in the 2020s, while a crater lake used as control is stable.
```

<!-- field: recommendation -->
### Recommendations (textarea, required)

```
Monitor these wetlands by how far they fill each spring against a fixed reference period, using every satellite scene, rather than by the area on one date per year, which depends on the date chosen. Treat the collapse as a water-balance problem: test the water-use explanation with groundwater levels, abstraction and irrigated-area data from DSİ, which this work did not have. Do not expect wet years to restore the wetlands: the Climate Digital Twin projects 14-16% less precipitation and summers 2.3-2.9 degC warmer by the 2040s for the basin. Keep a stable reference lake, such as Acıgöl (Karapınar), in any monitoring design.
```

<!-- field: conditions -->
### Conditions under which the synthesis applies (textarea, required)

```
Shallow, mostly precipitation- and groundwater-fed wetlands of the Konya Closed Basin, Central Anatolia (HydroBASINS endorheic basin 2040085960): Akgöl, Hotamış, Meke, Meyil and Bolluk, with Acıgöl (Karapınar) as control. Landsat 4-9 Collection 2 surface reflectance, NDWI, HEALPix cells of about 25 m, 1984-2025; ERA5-Land basin means for water years 1991-2025; Climate DT generation 2 (IFS-FESOM, IFS-NEMO) for the 2040s.
```

<!-- field: limitations -->
### Limitations of the synthesis (textarea, required)

```
Water use is inferred from what climate fails to explain, not measured: no groundwater, abstraction or irrigation data were used. The climate record starts in 1991, after much of the decline at Akgöl. NDWI misses bright or turbid water in some scenes. The site sets differ from those of the original papers (Özgencil et al. used seven bird-area lakes listed in their supplement), and their images and thresholds were not available. One basin; the conclusions may not transfer to wetlands fed mainly by rivers.
```

<!-- field: date -->
### Completion date (text input, required)

```
2026-10-23
```

<!-- field: source -->
### Supporting sources (text input, required)

The "drying" Outcome is appended by the wizard. Paste the other two Outcome URIs here (step 05 of `nanopubs/PUBLISHED.md` and of `nanopubs/drafts-climate/PUBLISHED.md`), one per bullet, before building the "drying" chain.

- _Source URL 1 (Outcome of the main chain): ___
- _Source URL 2 (Outcome of chain "climate"): ___

<!-- field: topic -->
### Topic (search/select, required)

Checked with `wikidata_lookup` (2026-10-24).

- wetland (Q170321)
- climate change (Q125928)

## Publication note

After publishing, paste the resulting URI into `nanopubs/drafts-drying/PUBLISHED.md` step 08.

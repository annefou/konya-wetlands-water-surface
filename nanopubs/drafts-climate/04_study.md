# 04 — FORRT Replication Study

Method read from `pipeline/basin.py`, `pipeline/04a_era5land_monthly.py`, `pipeline/04b_climatedt_monthly.py`, `pipeline/04c_water_balance.py` and `pipeline/02_analyse.py` (2026-10-24).

## Field-by-field draft

<!-- field: study -->
### Short URI suffix for study ID (text input, required)

```
konya-wetland-decline-meteorology-replication-study
```

<!-- field: label -->
### Label/name of replication study (text input, required)

```
Test of the climate explanation for the Konya Closed Basin wetland decline with an ERA5-Land water balance, 1991-2025
```

<!-- field: type -->
### Choose the study type (dropdown, required)

Different data (reanalysis instead of two stations) and a different method (water balance and wet-year comparison instead of visual comparison): a replication.

- [x] Replication Study - replication with different methodology or conditions
- [ ] Reproduction/Replication Study - study that is both, reproduction and replication
- [ ] Reproduction Study - direct reproduction: same methodology, same tools

<!-- field: claim -->
### Choose FORRT claim (search/select, required)

```
«URI of step 03 (FORRT Claim), filled by the chain wizard»
```

<!-- field: scope -->
### Describe what part of the claim is reproduced/replicated. (textarea, required)

```
The statement that the decrease of water surface in Akgöl wetland matches the meteorological conditions. In scope: whether precipitation, evaporation, potential evaporation and summer temperature over the Konya Closed Basin changed over 1991-2025 in a way that explains the loss, and whether the collapsed wetlands still fill in years as wet as before. Out of scope: the period before 1991, the paper's station records, and a direct attribution to irrigation or groundwater abstraction, for which no data were used.
```

<!-- field: methodology -->
### Describe how the claim is reproduced/replicated. (textarea, required)

```
ERA5-Land monthly means (precipitation, evaporation, potential evaporation, 2 m temperature) are sampled onto the 1,442 HEALPix cells (depth 10, about 6.4 km, WGS84 ellipsoid, nested) of the HydroBASINS endorheic basin 2040085960 and averaged over the basin per water year (October-September), 1991-2025. ERA5-Land has no irrigation, so its evaporation is that of the natural land surface. Trends are Theil-Sen slopes per decade with 95% intervals, plus 2016-2025 against 1991-2000. Wet-year test: for the four wetlands that stopped filling (Akgöl, Hotamış, Meke, Meyil), the spring maximum water area from every valid Landsat scene (NDWI > 0, HEALPix depth 18) as a percentage of its 1984-1995 reference, averaged over the wettest third of water years 1991-2005 and of 2011-2025. Climate DT generation 2 (IFS-FESOM, IFS-NEMO) gives the change to the 2040s against each model's own 1991-2020.
```

<!-- field: deviation -->
### Describe any deviations from original methodology. (textarea, optional)

```
The paper compares the four image dates with temperature and precipitation at the Konya and Ereğli stations, 1971-2015, by inspection. This study uses a basin-wide reanalysis water balance from 1991, formal trends, and a comparison of wet years, and adds a climate projection to the 2040s.
```

<!-- field: keyword -->
### Search keywords (Wikidata) (search/select, optional)

Checked with `wikidata_lookup` (2026-10-24).

- wetland (Q170321)
- climate change (Q125928)
- remote sensing (Q199687)

<!-- field: discipline -->
### Search discipline (Wikidata) (search/select, optional)

- hydrology (Q42250)

## Publication note

After publishing, paste the resulting URI into `nanopubs/drafts-climate/PUBLISHED.md` step 04.

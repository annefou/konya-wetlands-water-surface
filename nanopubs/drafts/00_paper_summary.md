# Paper summary

> Working scratchpad for the paper-analysis phase; it feeds the Quote / AIDA / Claim drafts and is not itself a nanopub.

**Reference paper:** Long-Term Monitoring of Wetlands via Remote Sensing and GIS: A Case Study from Turkey

**DOI:** 10.17501/iccc.2018.2102

**Authors:** Nebiye Musaoğlu, Ayşegül Tanık, M. Ümit Gümüşay, Adalet Dervişoğlu, B. Baha Bilgilioğlu, Nur Yağmur, Tolga Bakırman, Duygu Baran, M. Fatih Gökdağ (Istanbul Technical University; Yıldız Technical University)

**Year:** 2018 (*Proceedings of the 2nd International Conference on Climate Change*, vol. 2, pp. 11–21, TIIKM)

## Headline claim

> One of the important wetlands of the basin named as Akgol Wetland has almost lost its water surface by 96% at the same time interval, and is in danger of extinction.

Verified with `verify_quote` against `paper/musaoglu-2018.pdf` (page 1, abstract; SHA-256 31e67907…572df0c).

## Methodology summary

- **Data sources:** one Landsat image each for 1987 and 1998 (Landsat 5 TM), 2007 (Landsat 7 ETM+) and 2017 (Landsat 8 OLI); State Meteorological Service temperature and precipitation for Konya and Ereğli, 1971–2015.
- **Method:** NDWI = (Green − NIR)/(Green + NIR) in ERDAS 2016, water above a threshold chosen per image; areas compared between the four years.
- **Headline numbers:** Akgöl 2958.4 ha (1987), 1153.9 (1998), 12.7 (2007), 117.2 (2017), i.e. −96 % from 1987 to 2017; all basin water bodies about −23.5 % over 30 years.

## Replication design choice

- [ ] **Reproduction Study**
- [ ] **Replication Study**
- [x] **Reproduction/Replication Study**

Same sensor family and index (reproduction), but every valid Landsat scene from 1984 to 2025 instead of one per year, a fixed threshold with sensitivity, HEALPix cells, and the basin figure from JRC Global Surface Water (replication).

## Notes for downstream drafts

- The paper writes "Akgol" and "Turkey"; quotes stay verbatim, our text writes "Akgöl" and "Türkiye".
- Closest scenes (depth 18): 3006.8 ha (9 June 1987), 827.7 (7 June 1998, below the paper's 1153.9; 1151.9 at NDWI > −0.1), 9.3 (31 May 2007), 94.8 (27 June 2017); 1987→2017 −96.8 %. Medians of spring maxima 1984–95 vs 2015–25: 3423 → 299 ha, −91.3 %. Akgöl has not filled to half its 1984–95 level in any year since 2000.
- Basin: JRC −20.0 % (1984–2021), −40.4 % without Tuz Gölü.
- The paper also says the decrease "is matched with the meteorological conditions"; our water balance (`04c_water_balance.py`) qualifies that. It is a candidate for a second chain, not part of this one.
- Paper PDF is local only (`paper/*.pdf` git-ignored).

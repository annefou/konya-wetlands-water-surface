# Charts of the LifeWatch ERIC country file for Türkiye

Each chart in the country file is a small JSX module (Claude Docs widget) that draws an SVG from inline rows.
The rows are copies of the committed results files below, written by the scripts listed; the same rows also give the PNG.

| Chart code | Section | Rows | Written by | PNG |
| --- | --- | --- | --- | --- |
| [konya-wetlands-fill.jsx](konya-wetlands-fill.jsx) | 3.2 | `results/doc_figure_fill.json` | `pipeline/99_doc_figures.py` | `figures/doc_fill.png` |
| [akgol-scenes-vs-paper.jsx](akgol-scenes-vs-paper.jsx) | 3.2 | `results/doc_figure_akgol_scenes.csv` | `pipeline/99_doc_figures.py` | `figures/akgol_scenes.png` |
| [konya-rain-vs-fill.jsx](konya-rain-vs-fill.jsx) | 3.2 | `results/doc_figure_water_balance.json` | `pipeline/04c_water_balance.py` | `figures/water_balance.png` |

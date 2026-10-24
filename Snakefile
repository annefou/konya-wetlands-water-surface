# Snakefile: the whole Konya Closed Basin replication, in the order the results in results/ were produced.
#
#   pixi run snakemake --cores 1             # open data only: Landsat, JRC Global Surface Water, HydroBASINS
#   pixi run snakemake --cores 1 climate     # adds the basin water balance (CDS account; DestinE upgraded access)
#   pixi run snakemake --cores 1 -n          # dry run
#
# Downloads go to work/ (not committed). Landsat Collection 2 comes from Microsoft Planetary Computer (anonymous);
# accounts are read from ~/.cdsapirc (ERA5-Land) and ~/.polytopeapirc (Climate DT), never copied here.
# The Landsat step is long (every valid scene 1984-2025 for six sites) and resumable.

W = "work"
DT_MODELS = ["IFS-FESOM", "IFS-NEMO"]


rule all:
    input:
        "results/claims.json", "results/site_years.csv", "results/basin_jrc.json",
        "results/doc_figure_fill.json", "results/doc_figure_akgol_scenes.csv",


rule climate:
    input: rules.all.input, "results/water_balance_claims.json", "results/doc_figure_water_balance.json"


rule aoi:
    output: "results/sites_jrc.json"
    shell: "python pipeline/00_aoi.py {W}"

rule landsat:                       # every valid Landsat scene per site, resampled onto HEALPix depth 17
    input: "results/sites_jrc.json"
    output: f"{W}/landsat/scenes.csv"
    shell: "python pipeline/01_landsat_scenes.py {W}"

rule analyse:
    input: f"{W}/landsat/scenes.csv"
    output: "results/claims.json", "results/site_years.csv", "results/akgol_paper_years.csv"
    shell: "python pipeline/02_analyse.py {W}"

rule basin_jrc:                     # JRC Global Surface Water transitions over HydroBASINS 2040085960
    output: "results/basin_jrc.json"
    shell: "python pipeline/03_basin_jrc.py {W}"

rule era5land_monthly:
    output: f"{W}/wb/era5land_monthly_1990_2025.nc"
    shell: "python pipeline/04a_era5land_monthly.py {W}"

rule climatedt_monthly:             # region cut out by Polytope; resumable, one file per year
    output: expand(f"{W}/wb/dt_{{model}}/{{year}}.npz", model=DT_MODELS, year=range(1990, 2050))
    shell: " && ".join(f"python pipeline/04b_climatedt_monthly.py {W} {m}" for m in DT_MODELS)

rule water_balance:
    input: rules.era5land_monthly.output, rules.climatedt_monthly.output, "results/site_years.csv"
    output: "results/water_balance_claims.json", "results/water_balance_annual.csv",
            "results/doc_figure_water_balance.json", "figures/water_balance.png"
    shell: "python pipeline/04c_water_balance.py {W}"


# ---------- figures of the country file (rows + PNGs; the chart code is in docs/country_file/) ----------
rule doc_figures:
    input: "results/site_years.csv", f"{W}/landsat/scenes.csv"
    output: "results/doc_figure_fill.json", "results/akgol_scenes.csv", "results/doc_figure_akgol_scenes.csv",
            "figures/doc_fill.png"
    shell: "python pipeline/99_doc_figures.py {W}"

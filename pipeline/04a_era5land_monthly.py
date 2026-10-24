"""ERA5-Land monthly means over the Konya Closed Basin, 1990-2025 (Copernicus Climate Data Store, CC BY).

Variables (monthly_averaged_reanalysis, per day): total_precipitation (m), total_evaporation (m, negative =
evaporation), potential_evaporation (m, negative), 2m_temperature (K). ERA5-Land has no irrigation: its
evaporation is what the natural land surface would give with the observed weather. Area: the basin's bounding
box with 0.2 deg margin. Account read by cdsapi from ~/.cdsapirc (never copied here).

Usage: python pipeline/04a_era5land_monthly.py <ROOT>
Writes <ROOT>/wb/era5land_monthly_1990_2025.nc (not committed).
"""
import os
import sys

import cdsapi

ROOT = sys.argv[1]
OUT = f"{ROOT}/wb/era5land_monthly_1990_2025.nc"
AREA = [39.7, 29.8, 36.7, 35.3]          # N, W, S, E: HydroBASINS 2040085960 bounds 30.00-35.06 E, 36.90-39.49 N


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if os.path.exists(OUT):
        return
    cdsapi.Client(quiet=True).retrieve("reanalysis-era5-land-monthly-means", {
        "product_type": ["monthly_averaged_reanalysis"],
        "variable": ["total_precipitation", "total_evaporation", "potential_evaporation", "2m_temperature"],
        "year": [str(y) for y in range(1990, 2026)], "month": [f"{m:02d}" for m in range(1, 13)],
        "time": ["00:00"], "area": AREA, "data_format": "netcdf", "download_format": "unarchived"}, OUT)


if __name__ == "__main__":
    main()

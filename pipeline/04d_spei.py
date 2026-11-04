"""Wet years by SPEI: did the wetlands fill less in years that were equally wet once evaporative demand counts?

SPEI (Standardized Precipitation-Evapotranspiration Index; Vicente-Serrano et al. 2010, J. Climate 23:1696,
doi:10.1175/2009JCLI2909.1) per water year (October-September), from the basin-mean ERA5-Land monthly series of
04c_water_balance.py: climatic water balance D = sum over the water year of (P - PET); a three-parameter
log-logistic distribution fitted to D over the WMO normal 1991-2020 by probability-weighted moments (the paper's
method); SPEI = the standard-normal quantile of its probability. Two potential evaporations:
  * Thornthwaite (1948) from monthly mean 2 m temperature, as in the SPEI paper, at the basin's central latitude
    (37.8 N); heat index from the 1991-2020 monthly climatology. This is the main variant.
  * ERA5-Land "pev" (as in 04c), for comparison only: its summer 2023 values are about half those of 2022 and 2024
    (July 153 against 271 and 270 mm) although August 2023 was the hottest month, so water year 2023 (233 mm of rain,
    the driest of the record) comes out "wet"; and its D is too skewed for the log-logistic fit (standardised anomaly
    used instead).
Wet years in 1991-2005 and 2011-2025: (a) the wettest third of 1991-2020 by SPEI; (b) SPEI >= +1.0 ("moderately
wet", the class boundary of the SPI/SPEI scale, McKee et al. 1993; WMO-No. 1090, 2012). For each, the spring fill
of the four collapsed wetlands (results/site_years.csv, as in 04c). Also: the SPEI of the precipitation-defined
wet years of 04c, to see whether the later ones were drier once evaporative demand counts.
Usage: python pipeline/04d_spei.py <ROOT>   (needs <ROOT>/wb/era5land_monthly_1990_2025.nc from 04a)
Writes results/spei_wet_years.json and results/spei_water_years.csv.
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy.special import gamma as G
from scipy.stats import norm, pearsonr

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wb", os.path.join(HERE, "04c_water_balance.py"))
wb = importlib.util.module_from_spec(spec); spec.loader.exec_module(wb)   # reads ROOT from sys.argv[1]

LAT = 37.8
REF = (1991, 2020)
PERIODS = ((1991, 2005), (2011, 2025))


def daylength_hours(lat, doy):
    decl = 0.409 * np.sin(2 * np.pi * doy / 365 - 1.39)
    ws = np.arccos(np.clip(-np.tan(np.radians(lat)) * np.tan(decl), -1, 1))
    return 24 / np.pi * ws


def thornthwaite(T):
    """Monthly PET (mm) from monthly mean temperature (degC), Thornthwaite 1948."""
    Tr = T[(T.index.year >= REF[0]) & (T.index.year <= REF[1])]
    clim = Tr.groupby(Tr.index.month).mean()
    I = float(((clim.clip(lower=0) / 5) ** 1.514).sum())
    a = 6.75e-7 * I ** 3 - 7.71e-5 * I ** 2 + 1.792e-2 * I + 0.49239
    mid = pd.to_datetime([pd.Timestamp(t.year, t.month, 15) for t in T.index])
    L = daylength_hours(LAT, mid.dayofyear.values)
    N = T.index.days_in_month.values
    return pd.Series(np.where(T.values > 0, 16 * (L / 12) * (N / 30) * (10 * T.clip(lower=0).values / I) ** a, 0.0),
                     index=T.index)


def loglogistic_pwm(x):
    """Three-parameter log-logistic by probability-weighted moments (Vicente-Serrano et al. 2010, eqs. 3-6)."""
    x = np.sort(np.asarray(x, float)); n = len(x)
    F = (np.arange(1, n + 1) - 0.35) / n
    w = [np.mean((1 - F) ** s * x) for s in range(3)]
    beta = (2 * w[1] - w[0]) / (6 * w[1] - w[0] - 6 * w[2])
    g = G(1 + 1 / beta) * G(1 - 1 / beta)
    alpha = (w[0] - 2 * w[1]) * beta / g
    gam = w[0] - alpha * g
    return alpha, beta, gam


def spei(D, ref):
    alpha, beta, gam = loglogistic_pwm(D.loc[ref[0]:ref[1]])
    if not (np.isfinite(beta) and beta > 1):
        # The log-logistic needs beta > 1 (finite mean); with a strongly skewed D the PWM fit fails. Fall back to the
        # standardised anomaly over the reference period, and say so. Ranks, hence any wettest-third result, are the
        # same under both, since both are monotonic in D.
        r = D.loc[ref[0]:ref[1]]
        return (D - r.mean()) / r.std(), {"fit": "log-logistic failed (beta = %.3g); standardised anomaly used" % beta}
    z = D.astype(float).copy()
    for y, x in D.items():
        p = 1 / (1 + (alpha / (x - gam)) ** beta) if x > gam else 1e-6
        z[y] = norm.ppf(min(max(p, 1e-6), 1 - 1e-6))
    return z, {"fit": "log-logistic (PWM)", "alpha": round(float(alpha), 2), "beta": round(float(beta), 3), "gamma": round(float(gam), 2)}


def main():
    m = wb.era5land(wb.basin.cells(wb.ROOT))
    m["PET_TH"] = thornthwaite(m["T"])
    wy = wb.water_year(m.index)
    n = m.groupby(wy).size()
    A = m.groupby(wy)[["P", "PET", "PET_TH"]].sum()[n == 12].loc[1991:2025]
    sy = pd.read_csv("results/site_years.csv")
    sy["pct"] = 100 * sy.spring_max_ha / sy.ref_spring_ha
    fill = sy[sy.site.isin(wb.COLLAPSED)].groupby("year").pct.mean()
    claims = json.load(open("results/water_balance_claims.json"))
    p_wet = {k: v["wet_years"] for k, v in claims["wet_year_fill"].items()}
    out = {"method": "SPEI per water year (Oct-Sep), log-logistic by PWM fitted 1991-2020 (Vicente-Serrano et al. 2010)",
           "variants": {}}
    table = A.copy()
    for name, pet in (("ERA5-Land pev", "PET"), ("Thornthwaite", "PET_TH")):
        D = A["P"] - A[pet]
        z, par = spei(D, REF)
        table[f"SPEI_{pet}"] = z.round(2)
        za = (D - D.loc[REF[0]:REF[1]].mean()) / D.loc[REF[0]:REF[1]].std()
        res = {"PET_mean_1991_2020_mm": round(float(A[pet].loc[REF[0]:REF[1]].mean())), "loglogistic": par,
               "check_r_with_plain_standardised_D": round(float(pearsonr(z, za)[0]), 3),
               "PET_change_2016_2025_vs_1991_2000_mm": round(float(A[pet].loc[2016:2025].mean() - A[pet].loc[1991:2000].mean())),
               "SPEI_of_precipitation_wet_years": {k: {"years": v, "spei": [round(float(z[y]), 2) for y in v],
                                                       "mean": round(float(np.mean([z[y] for y in v])), 2)} for k, v in p_wet.items()}}
        thr = float(z.loc[REF[0]:REF[1]].quantile(2 / 3))
        for label, cut in (("wettest third 1991-2020", thr), ("SPEI >= +1.0", 1.0)):
            r = {"threshold_spei": round(cut, 2)}
            for a, b in PERIODS:
                wet = [int(y) for y in z.loc[a:b].index if z[y] >= cut]
                f = fill.reindex(wet).dropna()
                r[f"{a}-{b}"] = {"wet_years": wet, "spei": [round(float(z[y]), 2) for y in wet],
                                 "precip_mm": [round(float(A.loc[y, 'P'])) for y in wet],
                                 "mean_spring_fill_pct_4_sites": round(float(f.mean()), 1) if len(f) else None,
                                 "years_with_fill_data": int(len(f))}
            res[label] = r
        out["variants"][name] = res
    table.round(1).to_csv("results/spei_water_years.csv", index_label="water_year")
    json.dump(out, open("results/spei_wet_years.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

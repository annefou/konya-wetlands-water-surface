"""Climate DT generation 2 monthly means over the Konya Closed Basin, 1990-2049, both models.

Stream clmn (monthly means), resolution high (HEALPix depth 10 on a sphere), realization 1; historical 1990-2014,
SSP3-7.0 2015-2049. Parameters by numeric id (short names can resolve to other fields): 235055 avg_tprate
(precipitation rate), 235043 avg_ie (moisture flux, negative = evaporation), 228004 avg_2t (2 m temperature);
all kg m-2 s-1 or K. Only the basin's bounding box is requested (Polytope boundingbox feature). The samples are
the sphere cell centres; healpix-connector's BilinearConservative puts them on the basin's WGS84 cells (never by
matching ids). Account: DestinE upgraded access via ~/.polytopeapirc (never copied here).

Usage: python pipeline/04b_climatedt_monthly.py <ROOT> <MODEL> [<Y0> <Y1>]
Writes <ROOT>/wb/dt_<MODEL>/<year>.npz: pr, evap (mm per month, evaporation positive), t2m (degC), arrays
(12, cells) on the basin cells (pipeline/basin.py).
Raw responses are deleted; Climate DT data are not redistributed (DestinE terms).
"""
import calendar
import json
import os
import sys
import time

import numpy as np
from healpix_connector.resampling import BilinearConservative

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import basin  # noqa: E402

ROOT, MODEL = sys.argv[1], sys.argv[2]
Y0, Y1 = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1990, 2049)
OUT = f"{ROOT}/wb/dt_{MODEL}"
ENDPOINT = {"IFS-NEMO": "polytope.mn5.apps.dte.destination-earth.eu",
            "IFS-FESOM": "polytope.lumi.apps.dte.destination-earth.eu"}[MODEL]
BOX = [[39.7, 29.8], [36.7, 35.3]]          # [lat, lon] NW and SE corners
PARAMS = {"235055": "avg_tprate", "235043": "avg_ie", "228004": "avg_2t"}
BASE = {"class": "d1", "dataset": "climate-dt", "type": "fc", "expver": "0001", "generation": "2", "realization": "1",
        "model": MODEL, "resolution": "high", "stream": "clmn", "levtype": "sfc"}


def retrieve(client, req, target):
    for attempt in range(6):
        try:
            client.retrieve("destination-earth", req, target)
            return
        except (Exception, SystemExit) as e:          # the polytope client exits on a refusal
            print("retry", MODEL, req.get("year"), req.get("param"), attempt, type(e).__name__, str(e)[:200], flush=True)
            time.sleep(60 * (attempt + 1))
    raise RuntimeError(f"Climate DT request failed: {MODEL} {req.get('year')} {req.get('param')}")


def read(path, name):
    d = json.load(open(path))
    months, vals, pts = [], [], None
    for c in d["coverages"]:
        p = np.array([q[:2] for q in c["domain"]["axes"]["composite"]["values"]], float)
        if pts is None:
            pts = p
        assert np.array_equal(p, pts)
        months.append(c["domain"]["axes"]["t"]["values"][0][:7])
        vals.append(np.array(c["ranges"][name]["values"], float))
    o = np.argsort(months)
    return np.array(months)[o], np.stack(vals)[o], pts


def main():
    from polytope.api import Client
    os.makedirs(OUT, exist_ok=True)
    cells = basin.cells(ROOT)
    client = Client(address=ENDPOINT, quiet=True)
    op, grid = None, None
    for year in range(Y0, Y1 + 1):
        fn = f"{OUT}/{year}.npz"
        if os.path.exists(fn):
            continue
        t0 = time.time()
        exp = {"activity": "baseline", "experiment": "hist"} if year <= 2014 else \
              {"activity": "projections", "experiment": "SSP3-7.0"}
        out = {}
        for pid, name in PARAMS.items():
            raw = f"{OUT}/{year}_{pid}.covjson"
            retrieve(client, {**BASE, **exp, "param": pid, "year": str(year), "month": "/".join(str(m) for m in range(1, 13)),
                              "feature": {"type": "boundingbox", "points": BOX}}, raw)
            months, v, pts = read(raw, name)
            assert len(months) == 12, f"{MODEL} {year} {name}: {len(months)} months"
            if op is None:
                op = BilinearConservative(pts[:, 1], pts[:, 0], cells, basin.DEPTH)
                grid = pts
            assert np.array_equal(pts, grid)
            out[name] = op(v)[0]
            os.remove(raw)
        days = np.array([calendar.monthrange(year, m)[1] for m in range(1, 13)])[:, None] * 86400.0
        np.savez_compressed(fn, pr=(out["avg_tprate"] * days).astype(np.float32),
                            evap=(-out["avg_ie"] * days).astype(np.float32),
                            t2m=(out["avg_2t"] - 273.15).astype(np.float32))
        print("OK", MODEL, year, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

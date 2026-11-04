"""Rewrite the inline rows of the country-file charts from the committed results (run after the pipeline).

konya-wetlands-fill.jsx   <- results/doc_figure_fill.json            (site, year, pct, collapsed)
konya-rain-vs-fill.jsx    <- results/doc_figure_water_balance.json   (year, precip, fill) + wet, period from
                             results/water_balance_claims.json (wet = one of the wettest third of water years of
                             1991-2005 or 2011-2025; period = early 1991-2005, mid 2006-2010, late 2011-2025)
akgol-scenes-vs-paper.jsx <- paper rows from results/claims.json (fits = paper value within the range of that
                             year's valid scenes); the scene rows are results/doc_figure_akgol_scenes.csv, uploaded
                             to the doc as a CSV file (blob), so only its blob reference changes there.
Only the data arrays are replaced; the drawing code is left as it is.
Usage: python docs/country_file/write_rows.py   (from the repository root)
"""
import json
import re
from pathlib import Path

D = Path("docs/country_file")


def js(v):
    if v is None:
        return "null"
    if isinstance(v, str):
        return "'" + v.replace("'", "\\'") + "'"
    return repr(round(v, 1)) if isinstance(v, float) else str(v)


def array(rows, keys):
    return "[" + ",".join("{" + ", ".join(f"{k}:{js(r[k])}" for k in keys) + "}" for r in rows) + "]"


def replace_source(path, name, new_array):
    s = path.read_text()
    m = re.search(rf"{name}:\{{kind:'data', data:\[", s)
    start = m.end() - 1
    depth, i = 0, start
    while True:
        if s[i] == "[":
            depth += 1
        elif s[i] == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1
    path.write_text(s[:start] + new_array + s[i + 1:])
    return new_array


def fill_rows():
    rows = json.loads(Path("results/doc_figure_fill.json").read_text())
    return array(rows, ["site", "year", "pct", "collapsed"])


def rain_rows():
    rows = json.loads(Path("results/doc_figure_water_balance.json").read_text())
    wet = {y for v in json.loads(Path("results/water_balance_claims.json").read_text())["wet_year_fill"].values()
           for y in v["wet_years"]}
    out = [{"year": r["year"], "precip": r["precip_pct"], "fill": r["fill_pct"], "wet": int(r["year"] in wet),
            "period": "early" if r["year"] <= 2005 else ("mid" if r["year"] <= 2010 else "late")} for r in rows]
    return array(out, ["year", "precip", "fill", "wet", "period"])


def paper_rows():
    c = json.loads(Path("results/claims.json").read_text())["C1_akgol_paper_years"]
    out = [{"year": r["year"], "ha": r["paper_ha"], "fits": "yes" if r["paper_within_range"] else "no"} for r in c]
    return array(out, ["year", "ha", "fits"])


def main():
    new = {"konya-wetlands-fill.jsx": {"rows": fill_rows()},
           "konya-rain-vs-fill.jsx": {"rows": rain_rows()},
           "akgol-scenes-vs-paper.jsx": {"paper": paper_rows()}}
    for f, sources in new.items():
        for name, arr in sources.items():
            replace_source(D / f, name, arr)
    Path("docs/country_file/rows.json").write_text(json.dumps(new, indent=1, ensure_ascii=False))
    print({f: {k: v.count("},{") + 1 for k, v in s.items()} for f, s in new.items()})


if __name__ == "__main__":
    main()

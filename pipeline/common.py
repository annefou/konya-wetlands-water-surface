"""Shared definitions: sites, HEALPix grid (healpix-geo, WGS84 ellipsoid, NESTED) and the resampler.

No science choices here beyond the site list; thresholds and methods live in the step scripts.
"""
from __future__ import annotations

import numpy as np
import healpix_geo.nested as hn

DEPTH = 17                       # ~49 m cells (0.24 ha) on the WGS84 ellipsoid
ELLIPSOID = "WGS84"
WGS84_A = 6378137.0
WGS84_F = 1 / 298.257223563

# Seed points (OpenStreetMap / Nominatim, checked 2026-10-23) and why each site is in the test
SITES = {
    "akgol":   {"name": "Akgöl (Ereğli)", "lon": 33.758, "lat": 37.521,
                "why": "Musaoğlu et al. 2018: 2958.4 ha (1987) -> 117.2 ha (2017)"},
    "hotamis": {"name": "Hotamış (Çumra)", "lon": 33.052, "lat": 37.557, "why": "Konya Closed Basin wetland"},
    "meke":    {"name": "Meke (Karapınar)", "lon": 33.640, "lat": 37.685, "why": "Ramsar site (2005), crater lake"},
    "acigol_k": {"name": "Acıgöl (Karapınar)", "lon": 33.666, "lat": 37.713, "why": "crater lake, reference for a stable lake"},
    "meyil":   {"name": "Meyil (Karatay)", "lon": 33.354, "lat": 37.988,
                "why": "ciliate survey by Çapar Dinçer (Hacettepe), 2013-2014"},
    "bolluk":  {"name": "Bolluk (Cihanbeyli)", "lon": 32.934, "lat": 38.540,
                "why": "ciliate survey by Çapar Dinçer (Hacettepe), 2013-2014"},
}


def authalic_radius(a: float = WGS84_A, f: float = WGS84_F) -> float:
    e2 = f * (2 - f)
    e = np.sqrt(e2)
    q_p = 1 + (1 - e2) / (2 * e) * np.log((1 + e) / (1 - e))
    return float(a * np.sqrt(q_p / 2))


def cell_area_ha(depth: int = DEPTH) -> float:
    return float(4 * np.pi * authalic_radius() ** 2 / (12 * 4 ** depth)) / 1e4


def polygon_cells(ring_lonlat: np.ndarray, depth: int = DEPTH) -> np.ndarray:
    ids, _, _ = hn.polygon_coverage(np.asarray(ring_lonlat, float), depth, ellipsoid=ELLIPSOID, flat=True)
    return np.unique(np.asarray(ids, np.uint64))


def cell_centres(ids: np.ndarray, depth: int = DEPTH):
    lon, lat = hn.healpix_to_lonlat(np.asarray(ids, np.uint64), depth, ellipsoid=ELLIPSOID)
    return np.asarray(lon), np.asarray(lat)


class BilinearToCells:
    """healpix-resample BilinearResampler in conservative mode from source pixel centres onto fixed cells.

    Mean of an intensive field (reflectance) = resample(value) / resample(valid ones); missing pixels (cloud,
    shadow, fill, Landsat 7 stripes) are excluded and reported as a per-cell valid share. Never a PSF kernel.
    """

    def __init__(self, lon, lat, cell_ids, depth: int = DEPTH):
        from healpix_resample import BilinearResampler
        self.op = BilinearResampler(lon_deg=np.asarray(lon, float), lat_deg=np.asarray(lat, float), level=depth,
                                    nest=True, ellipsoid=ELLIPSOID, verbose=False, area=np.ones(len(lon)))
        self.cell_ids = np.asarray(cell_ids, np.uint64)
        ones = self.op.resample(np.ones(len(lon)), conservative=True)
        self._full = self._place(ones)

    def _place(self, res) -> np.ndarray:
        cid = np.asarray(res.cell_ids, np.uint64)
        out = np.full(len(self.cell_ids), np.nan)
        pos = np.clip(np.searchsorted(self.cell_ids, cid), 0, len(self.cell_ids) - 1)
        hit = self.cell_ids[pos] == cid
        out[pos[hit]] = np.asarray(res.cell_data, float)[hit]
        return out

    def __call__(self, values):
        v = np.asarray(values, float)
        num = self._place(self.op.resample(v, conservative=True))
        den = self._place(self.op.resample(np.where(np.isfinite(v), 1.0, np.nan), conservative=True))
        with np.errstate(invalid="ignore", divide="ignore"):
            return num / den, den / self._full        # mean, valid share

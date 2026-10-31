import json
import numpy as np

DAYS_IN_MONTH = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ---------------------------------------------------------------- LOADING DATASET
def load_data(path):
    data = np.load(path)
    load = data["load_kw"].astype(np.float64)
    grid = data["grid_available"].astype(bool)
    solar = data["solar_kw_per_kwp"].astype(np.float64)
    params = json.loads(str(data["params_json"]))
    return load, grid, solar, params

# ---------------------------------------------------------------- RESHAPE
def to_grid(flat):
    n_days = flat.size // 48
    out = flat.reshape(n_days, 48)
    assert out.shape == (n_days, 48)
    return out

# ---------------------------------------------------------------- STAGE 2
def find_watts_days(load):
    """Problem 1: a month logged in watts.  (365,48) -> (365,) bool"""
    daily_total = load.sum(axis=1)
    typical = np.nanmedian(daily_total)
    return daily_total > 100 * typical          # nan > number is False


def find_stuck_days(load):
    """Problem 2: meter stuck on one value.  (365,48) -> (365,) bool
    A 'stuck' stretch = at least one full day (48 readings) of identical values."""
    flat = load.ravel()
    same = np.concatenate(([False], flat[1:] == flat[:-1], [False])).astype(int)
    edges = np.diff(same)
    starts = np.flatnonzero(edges == 1)          # where a run of repeats begins
    ends = np.flatnonzero(edges == -1)           # where it stops
    long_runs = (ends - starts + 1) >= 48
    stuck = np.zeros(flat.size, dtype=bool)
    for s, e in zip(starts[long_runs], ends[long_runs]):   # only a handful of runs
        stuck[s:e + 1] = True
    return stuck.reshape(load.shape).any(axis=1)

# ---------------------------------------------------------------- FIXING PROBLEM 3
def find_missing_days(load):
    return np.isnan(load).any(axis=1)

# ---------------------------------------------------------------- DATA CLEANING (ALL 3)
def clean_load(load):
    report = {}
    watts = find_watts_days(load)
    report["watts_days"] = np.flatnonzero(watts)
    fixed = load.copy()
    fixed[watts] = fixed[watts] / 1000.0                    # W -> kW

    missing = find_missing_days(fixed)
    stuck = find_stuck_days(fixed)
    report["missing_days"] = np.flatnonzero(missing)
    report["stuck_days"] = np.flatnonzero(stuck)

    bad = missing | stuck
    n_days = fixed.shape[0]
    out = fixed.copy()
    for d in np.flatnonzero(bad):
        cand = [d + k for k in (-7, 7, -14, 14)
                if 0 <= d + k < n_days and not bad[d + k]][:2]
        out[d] = fixed[cand].mean(axis=0)
    assert out.shape == load.shape
    assert not np.isnan(out).any()
    return out, report


"""
Project 6 - Energy: grid, generator & solar for Eko Grand Hotel
NumPy + Matplotlib only (plus json to read the settings).
"""
import json
import numpy as np

DAYS_IN_MONTH = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ---------------------------------------------------------------- LOADING DATASET
def load_data(path):
"""Open the .npz file.  path -> (load, grid, solar, params)
    load  (17520,) float64 | grid (17520,) bool | solar (17520,) float64"""
    data = np.load(path)
    load = data["load_kw"].astype(np.float64)
    grid = data["grid_available"].astype(bool)
    solar = data["solar_kw_per_kwp"].astype(np.float64)
    params = json.loads(str(data["params_json"]))
    return load, grid, solar, params

# ---------------------------------------------------------------- RESHAPE
def to_grid(flat):
    """Give the flat stream its structure.  (17520,) -> (365, 48)"""
    assert flat.size % 48 == 0, "data must be a whole number of days"
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
    """Problem 3: a day that is nan.  (365,48) -> (365,) bool"""
    return np.isnan(load).any(axis=1)
# ---------------------------------------------------------------- DATA CLEANING (ALL 3)
def clean_load(load):
    """Fix all three problems.  (365,48) -> (365,48), plus a report dict."""
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
    """pick neighbours from the *good* days only"""
    n_days = fixed.shape[0]
    out = fixed.copy()
    for d in np.flatnonzero(bad):
        cand = [d + k for k in (-7, 7, -14, 14)
                if 0 <= d + k < n_days and not bad[d + k]][:2]
        out[d] = fixed[cand].mean(axis=0)
    assert out.shape == load.shape
    assert not np.isnan(out).any()
    return out, report

# ---------------------------------------------------------------- ANALYSIS
def energy_split(load_kw, grid_on):
    """kW -> kWh (x0.5h) and split by grid.  (365,48) each ->
    kwh, kwh_grid_on, kwh_grid_off   all (365,48)"""
    kwh = load_kw * 0.5
    return kwh, np.where(grid_on, kwh, 0.0), np.where(~grid_on, kwh, 0.0)
 
 
def month_index(n_days=365):
    """Month number (0-11) for each day.  -> (365,)"""
    return np.repeat(np.arange(12), DAYS_IN_MONTH)[:n_days]
 
 
def monthly_sum(per_day):
    """(365,) -> (12,)"""
    return np.bincount(month_index(per_day.size), weights=per_day, minlength=12)
 
 
# ---------------------------------------------------------------- ANALYSIS (SOLAR SCENARIO)
def solar_scenario(load_kw, grid_on, solar_per_kwp, kwp, litres_per_kwh):
    """Solar first, then grid, then generator.
    In : load_kw, grid_on, solar_per_kwp all (365,48); kwp, litres_per_kwh scalars
    Out: dict of six arrays, each (365,48): solar_kwh, solar_used, wasted,
         from_grid, from_gen, diesel_l"""
    load_kwh = load_kw * 0.5
    solar_kwh = solar_per_kwp * kwp * 0.5
    solar_used = np.minimum(solar_kwh, load_kwh)            # cannot use more than needed
    wasted = solar_kwh - solar_used                         # surplus is lost
    shortfall = load_kwh - solar_used
    from_grid = np.where(grid_on, shortfall, 0.0)
    from_gen = np.where(~grid_on, shortfall, 0.0)
    out = dict(solar_kwh=solar_kwh, solar_used=solar_used, wasted=wasted,
               from_grid=from_grid, from_gen=from_gen,
               diesel_l=from_gen * litres_per_kwh)
    assert all(v.shape == load_kw.shape for v in out.values())
    return out

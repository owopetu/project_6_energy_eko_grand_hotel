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



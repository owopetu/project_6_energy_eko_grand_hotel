# Group 6: Hotel Energy Consumption and Solar Analysis

## Project Overview

This project analyses the electricity consumption and energy supply of a fictional hotel, **Eko Grand Hotel, Lagos**, using Python.

The hotel relies on a combination of grid electricity and a diesel-powered generator. The project investigates its annual electricity consumption, generator dependence, and the potential financial and operational benefits of introducing a reference solar energy system.

Using historical energy data for 2025, the analysis aims to answer two key business questions:

1. How much electricity does the hotel consume annually, how many hours does it experience grid outages, and how much diesel does its generator consume?
2. How much diesel could the hotel save by introducing solar energy, and what would those savings be worth in Nigerian Naira?

## Project Objectives

The main objectives are to:

- Examine and prepare the hotel's half-hourly energy data.
- Identify and correct data quality issues.
- Calculate annual electricity consumption in kWh.
- Determine the total hours without grid electricity.
- Estimate annual generator energy consumption and diesel usage.
- Identify the month with the highest generator energy demand.
- Model a reference solar installation and estimate its impact.
- Calculate potential diesel savings in litres, percentage terms, and monetary value.

## Libraries Used

- Python
- NumPy
- Matplotlib
- JSON

## Dataset

The project uses the supplied `group06_energy.npz` dataset, containing half-hourly energy observations for 2025.

The dataset includes:

- `load_kw`: Hotel electricity demand in kW.
- `grid_available`: Indicates whether grid electricity is available during each half-hour.
- `solar_kw_per_kwp`: Solar energy output per installed kWp.
- `year`: Reference year of the dataset.
- `params_json`: Contains the generator fuel-consumption parameter and reference solar installation capacity.

The original dataset is provided separately and is not included in this repository.

## Data Preparation

The analysis begins by reshaping the half-hourly observations into daily records, with 48 observations per day.

Three data quality issues are investigated and addressed:

1. A month recorded in watts instead of kilowatts.
2. A week of repeated readings caused by a meter issue.
3. A missing day of observations.

The corrections are applied before the energy calculations are performed.

## Analysis Pipeline

The main analysis is implemented in `group6_energy_analysis.py` through the `run_pipeline(path)` function.

The pipeline performs the following operations:

1. Loads the supplied energy dataset.
2. Prepares and cleans the energy observations.
3. Calculates annual electricity consumption.
4. Separates grid-supplied energy from generator-supplied energy.
5. Estimates diesel consumption using the supplied generator fuel-consumption parameter.
6. Calculates monthly generator energy consumption and identifies the month with the highest demand.
7. Models the reference solar installation, with solar serving hotel demand first.
8. Estimates generator diesel consumption under the solar scenario.
9. Calculates diesel savings in litres and percentage terms.
10. Estimates the monetary value of the diesel savings using a diesel price supplied to the pipeline.

## Running the Project

### Requirements

Ensure that Python and the following libraries are installed:

- NumPy
- Matplotlib

### Installation

Install the required libraries using:

```bash
pip install numpy matplotlib
```

### Running the Pipeline

Download or clone this repository and ensure that the supplied dataset is available locally.

Run the analysis using:

```python
from group6_energy_analysis import run_pipeline

results = run_pipeline(
    "path/to/group06_energy.npz",
    diesel_price_naira=1800
)
```

The diesel price shown above is an example input and should be updated to the researched price used in the final analysis.

The pipeline returns a dictionary containing the cleaned data, data-quality report, annual and monthly energy results, diesel consumption, solar scenario results, and estimated savings.

## Key Outputs

The pipeline produces the following results:

| Output | Description |
|---|---|
| `annual_kwh` | Annual hotel electricity consumption |
| `hours_off` | Total hours without grid electricity |
| `grid_kwh` | Electricity supplied by the grid |
| `gen_kwh` | Electricity supplied by the generator in the baseline scenario |
| `diesel_today` | Estimated baseline diesel consumption |
| `gen_by_month` | Monthly generator energy consumption |
| `worst_month` | Month with the highest generator energy demand |
| `diesel_solar` | Estimated diesel consumption with solar |
| `saved_l` | Diesel saved in litres |
| `saved_pct` | Percentage reduction in diesel consumption |
| `saved_naira` | Estimated monetary value of diesel savings |
| `gen_kwh_solar` | Generator energy required under the solar scenario |

## Project Team

**Group 6 — MSc Data Science**

- Member 1: Owopetu Caleb
- Member 2: Oyedele-Aro Olalekan
- Member 3: Suleiman Ahmed-Tijani
- Member 4: Udechukwu Chinaemerem
- Member 5: Umoru Oluwatobi
- Member 6: Tuggen Jonathan


## Academic Context

This project was completed as part of the Python Programming for Data Science course in the MSc Data Science programme at Pan-Atlantic University (PAU).

**Academic Year:** 2026

---

*This repository contains the group's Python implementation and supporting analysis for the hotel energy consumption and solar assessment project.*

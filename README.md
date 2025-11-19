
# RideWise:Predicting Bike-Sharing Demand Based on Weather and Urban Eventsac

## 📌 Project Overview

This project explores how weather, season, and time influence bike rental demand in Washington D.C. This dataset contains both hourly and daily logs, making it useful for understanding short-term trends (like peak commuting hours) as well as long-term seasonal changes.

My main aim in this stage was to prepare a clean, analysis-ready dataset that can later be used for forecasting daily or hourly rental counts.

---

## 📊 Dataset Description

The original dataset comes from the Capital Bikeshare program and includes two years of usage data (2011–2012). This dataset include combined bike usage logs with weather information, so it becomes possible to link temperature, humidity, rain, hour of the day, etc., to rental behavior.

There are two files:

* **day.csv** — one row per day
* **hour.csv** — one row per hour

Both contain fields like date, season, holiday, working day flag, temperature, humidity, windspeed, and rental counts. Only the hourly file contains the hour column.

I used both files and mearged them to create a richer dataset for modeling. because I wanted to understand the relationship between daily and hourly patterns.

---

## 📚 Dataset Source & Citation

This dataset was originally prepared by **Hadi Fanaee-T** from the University of Porto. Since the authors requested citation in any downstream use, I’ve included their reference below.

> Fanaee-T, Hadi, and Gama, Joao. (2013).
> *Event labeling combining ensemble detectors and background knowledge.*
> Progress in Artificial Intelligence.
> doi:10.1007/s13748-013-0040-3

I’ve also linked the Kaggle version for convenience.

Dataset: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset?select=hour.csv

---

## Preprocessing Steps 

* **Analyzed dataset structure** — Inspected null values, duplicates, and overall column distributions.
* **Standardized date format** — Converted `dteday` into a consistent `datetime` format across both datasets.
* **Validated logical consistency** — Checked conflicting cases (e.g., `holiday = 1` and `workingday = 1`).
* **Merged datasets** — Concatenated aligned datasets using `pd.concat()` to create a unified hourly–daily dataset.
* **Performed post-merge cleanup** — Removed duplicates, corrected datatypes, sorted by datetime, and exported the cleaned dataset.

---





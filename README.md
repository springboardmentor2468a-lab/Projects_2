# AI RideWise 🚲

AI RideWise is a compact, data-driven bike demand forecasting app that provides both day-wise and hour-wise predictions. It includes a Streamlit dashboard (`app.py`) for interactive forecasting and a polished static UI (`templates/index.html`) with a custom canvas bar chart showing sample or API-driven predictions.

---

## Features ✅

- Predicts bike demand hour-wise (next 6 hours) and day-wise (next 5 days)
- Streamlit dashboard with neat theme and responsive charts
- Offline sample chart (canvas) in `templates/index.html` for quick visual verification
- Time-series training helpers and optional model training scripts

---

## Quick start (Windows)

1. Clone the repo and move into the project directory:

```powershell
git clone <repo-url>
cd Ridewise
```

2. Create a virtual environment and activate it (Windows PowerShell):

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

If there is no `requirements.txt`, install at least:

```powershell
pip install streamlit pandas scikit-learn joblib matplotlib
```

4. Run the app:

```powershell
streamlit run app.py
```

Open the local server URL printed by Streamlit (usually http://localhost:8501).

---

## Files & Structure

- `app.py` — The Streamlit dashboard and modeling helpers.
- `templates/index.html` — Static front-end with a canvas bar chart (also useful for testing chart rendering).
- `static/` — Images and other static assets used by the front-end.
- `day.csv`, `hour.csv` — Example datasets used for training / time-series forecasting.
- `bike_demand_pipeline.pkl` — The production model (if present).

---

## Adjusting the canvas chart (HTML)

If you'd like to see the specific values you mentioned (Hour 11 → 70, Hour 12 → 80, Hour 13 → 82, Hour 14 → 82, Hour 15 → 83, Hour 16 → 85) directly on the page for quick verification, open `templates/index.html` and locate the sample data near the top of the script:

```js
let bars = [70, 80, 82, 82, 83, 85];
let labels = ['Hour 11','Hour 12','Hour 13','Hour 14','Hour 15','Hour 16'];
```

Refresh the page (Ctrl+F5) in your browser to see the updated sample chart with numeric labels shown above or inside the bars.

---

## Model training / retraining

- `train_day_ts_model()` and `train_hour_ts_model()` in `app.py` will train/save local Random Forest time-series models (`day_ts_model.pkl`, `hour_ts_model.pkl`) if not already present.
- To retrain, delete those `.pkl` files and run the relevant page action in the Streamlit UI.

---

## Development and contribution

- Create a branch for your work (`git checkout -b feat/your-feature`) and open a PR.
- Please include a short description, screenshots (if UI-related), and any test steps.

---

## Troubleshooting

- If `streamlit` doesn't start, ensure your virtual environment is active and dependencies are installed.
- If model files are missing (`bike_demand_pipeline.pkl`), the app may still run, but prediction endpoints or certain features will be limited.

---

## License & Credits

Include your preferred license file (e.g., `MIT`) and attribution if you used external datasets or code snippets.

---


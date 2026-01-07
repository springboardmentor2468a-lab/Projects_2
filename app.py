import streamlit as st
import pandas as pd
import pickle
import numpy as np
from datetime import date, timedelta

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Bike Rental Forecast", layout="wide")

st.title("🚲 Bike Rental Demand Forecast")
st.caption("Day-wise and Hour-wise predictions using separate trained models.")

# -------------------- LOAD MODELS --------------------
@st.cache_resource
def load_models():
    models = {}
    try:
        with open("hour_model.pkl", "rb") as f:
            models["hour"] = pickle.load(f)
    except:
        models["hour"] = None

    try:
        with open("day_model.pkl", "rb") as f:
            models["day"] = pickle.load(f)
    except:
        models["day"] = None

    return models

models = load_models()

# -------------------- SIDEBAR INPUTS --------------------
st.sidebar.header("Input Settings")

mode = st.sidebar.radio("Prediction Mode", ["Day", "Hour"])
selected_date = st.sidebar.date_input("Select Date", date.today())

season = st.sidebar.selectbox("Season", [1, 2, 3, 4])
holiday = st.sidebar.selectbox("Holiday", [0, 1])
workingday = st.sidebar.selectbox("Working Day", [0, 1])
weathersit = st.sidebar.selectbox("Weather Situation", [1, 2, 3, 4])

temp = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5)
atemp = st.sidebar.slider("Feels Like Temperature", 0.0, 1.0, 0.5)
hum = st.sidebar.slider("Humidity", 0.0, 1.0, 0.5)
windspeed = st.sidebar.slider("Windspeed", 0.0, 1.0, 0.2)

# -------------------- PREDICTION --------------------
if st.button("Predict Demand"):

    weekday = selected_date.weekday()
    mnth = selected_date.month

    # ====================== DAY MODE ======================
    if mode == "Day":
        if models["day"] is None:
            st.error("❌ day_model.pkl not found.")
        else:
            day_results = []

            # Baseline for lag & rolling features
            base_cnt = 400  

            for i in range(11):
                current_date = selected_date + timedelta(days=i)
                weekday_i = current_date.weekday()
                mnth_i = current_date.month

                # Cyclical encoding
                mnth_sin = np.sin(2 * np.pi * mnth_i / 12)
                mnth_cos = np.cos(2 * np.pi * mnth_i / 12)
                weekday_sin = np.sin(2 * np.pi * weekday_i / 7)
                weekday_cos = np.cos(2 * np.pi * weekday_i / 7)

                input_df = pd.DataFrame([{
                    "season": season,
                    "mnth": mnth_i,
                    "holiday": holiday,
                    "weekday": weekday_i,
                    "workingday": workingday,
                    "weathersit": weathersit,
                    "temp": temp,
                    "atemp": atemp,
                    "hum": hum,
                    "windspeed": windspeed,

                    # Lag & rolling features
                    "cnt_lag1": base_cnt,
                    "cnt_lag2": base_cnt,
                    "cnt_lag7": base_cnt,
                    "cnt_roll3": base_cnt,
                    "cnt_roll7": base_cnt,

                    # Cyclical features
                    "mnth_sin": mnth_sin,
                    "mnth_cos": mnth_cos,
                    "weekday_sin": weekday_sin,
                    "weekday_cos": weekday_cos
                }])

                pred = models["day"].predict(input_df)[0]
                base_cnt = int(pred)  # recursive forecasting

                day_results.append({
                    "Date": current_date.strftime("%d-%b-%Y"),
                    "Predicted Bike Demand": int(pred)
                })

            day_df = pd.DataFrame(day_results)

            st.subheader("📋 Day-wise Bike Demand (Selected Day + Next 10 Days)")
            st.dataframe(day_df, use_container_width=True)

            st.subheader("📊 Day-wise Demand Trend")
            st.line_chart(day_df.set_index("Date")["Predicted Bike Demand"])

    # ====================== HOUR MODE ======================
    else:
        if models["hour"] is None:
            st.error("❌ hour_model.pkl not found.")
        else:
            hourly_results = []

            for h in range(24):
                input_df = pd.DataFrame([{
                    "season": season,
                    "mnth": mnth,
                    "hr": h,
                    "holiday": holiday,
                    "weekday": weekday,
                    "workingday": workingday,
                    "weathersit": weathersit,
                    "temp": temp,
                    "atemp": atemp,
                    "hum": hum,
                    "windspeed": windspeed
                }])

                pred = models["hour"].predict(input_df)[0]

                hourly_results.append({
                    "Hour (1–24)": h + 1,
                    "Predicted Bike Demand": int(pred)
                })

            hour_df = pd.DataFrame(hourly_results)

            st.subheader("📋 Hour-wise Bike Demand (1–24 Hours)")
            st.dataframe(hour_df, use_container_width=True)

            st.subheader("📊 Hourly Demand Trend for Selected Day")
            st.line_chart(
                hour_df.set_index("Hour (1–24)")["Predicted Bike Demand"]
            )

    st.success("✅ Prediction completed successfully")

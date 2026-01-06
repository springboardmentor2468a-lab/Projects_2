import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bike Demand Predictor", layout="centered")
st.title("🚲 Bike Demand Predictor")
import base64
def set_bg_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp > .main > div {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 10px;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_local("bg.png")

@st.cache_resource
def load_models():
    return (
        pickle.load(open("day_model.pkl", "rb")),
        pickle.load(open("hour_model.pkl", "rb"))
    )

day_model, hour_model = load_models()

DAY_MAP = {
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6
}
DAY_MAP_REV = {v: k for k, v in DAY_MAP.items()}

# ---------------- Session state for clearing output ----------------
if "results" not in st.session_state:
    st.session_state.results = None
if "mode_prev" not in st.session_state:
    st.session_state.mode_prev = None

# ---------------- Mode selector OUTSIDE form ----------------
mode = st.selectbox("Prediction Type", ["Day (7 days)", "Hour (6 hours)"])

# Clear output when mode changes
if st.session_state.mode_prev != mode:
    st.session_state.results = None
st.session_state.mode_prev = mode

# ---------------- Form ----------------
with st.form("predict_form"):

    season = st.selectbox("Season (1–4)", [1, 2, 3, 4])
    mnth = st.slider("Month (1–12)", 1, 12, 7)
    holiday = st.selectbox("Holiday", [0, 1])
    workingday = st.selectbox("Working Day", [0, 1])
    weathersit = st.selectbox("Weather Situation", [1, 2, 3])
    temp = st.slider("Temperature", 0.0, 1.0, 0.5)
    atemp = st.slider("A-Temperature", 0.0, 1.0, 0.5)
    hum = st.slider("Humidity", 0.0, 1.0, 0.5)
    windspeed = st.slider("Wind Speed", 0.0, 1.0, 0.2)

    if mode == "Day (7 days)":
        day_name = st.selectbox("Current Day", list(DAY_MAP.keys()))
        current_day = DAY_MAP[day_name]
    else:
        hr_12 = st.selectbox("Hour (1–12)", list(range(1, 13)), index=11)
        meridiem = st.radio("AM / PM", ["AM", "PM"], horizontal=True)

        if hr_12 == 12:
            current_hr = 0 if meridiem == "AM" else 12
        else:
            current_hr = hr_12 if meridiem == "AM" else hr_12 + 12

    submit = st.form_submit_button("Predict")

# ---------------- Prediction ----------------
if submit:

    if mode == "Day (7 days)":
        weekdays = [(current_day + i) % 7 for i in range(7)]

        future_days = pd.DataFrame({
            "season": [season]*7,
            "mnth": [mnth]*7,
            "holiday": [holiday]*7,
            "weekday": weekdays,
            "workingday": [workingday]*7,
            "weathersit": [weathersit]*7,
            "temp": [temp]*7,
            "atemp": [atemp]*7,
            "hum": [hum]*7,
            "windspeed": [windspeed]*7
        })

        preds = np.expm1(day_model.predict(future_days))

        st.session_state.results = pd.DataFrame(
            preds,
            index=[DAY_MAP_REV[d] for d in weekdays],
            columns=["Predicted Bike Demand"]
        )

    else:
        next_hours = [((current_hr + i) % 24) for i in range(1, 7)]
        weekdays = [0]*6

        future_hours = pd.DataFrame({
            "season": [season]*6,
            "mnth": [mnth]*6,
            "hr": next_hours,
            "holiday": [holiday]*6,
            "weekday": weekdays,
            "workingday": [workingday]*6,
            "weathersit": [weathersit]*6,
            "temp": [temp]*6,
            "atemp": [atemp]*6,
            "hum": [hum]*6,
            "windspeed": [windspeed]*6
        })

        preds = np.expm1(hour_model.predict(future_hours))

        def fmt(h):
            if h == 0: return "12:00 AM"
            if h == 12: return "12:00 PM"
            return f"{(h-12 if h > 12 else h):02d}:00 {'PM' if h >= 12 else 'AM'}"

        st.session_state.results = pd.DataFrame(
            preds,
            index=[fmt(h) for h in next_hours],
            columns=["Predicted Bike Demand"]
        )

# ---------------- Display results ----------------
if st.session_state.results is not None:
    st.subheader("Prediction Results")
    st.dataframe(st.session_state.results)

    fig, ax = plt.subplots(figsize=(8, 4))
    if mode == "Day (7 days)":
        ax.bar(st.session_state.results.index, st.session_state.results.iloc[:, 0])
        plt.xticks(rotation=30, ha="right")
    else:
        ax.plot(st.session_state.results.index, st.session_state.results.iloc[:, 0], marker="o")
        plt.xticks(rotation=45)

    ax.set_ylabel("Bike Demand")
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
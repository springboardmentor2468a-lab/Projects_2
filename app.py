


import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="RideWise Bike Demand Forecasting",
    page_icon="🚲",
    layout="wide"
)


if "page" not in st.session_state:
    st.session_state.page = "home"


DAY_IMG = "https://c.ndtvimg.com/2024-06/n7kugs6o_world-motorcycle-day-2024_625x300_21_June_24.jpg?im=FaceCrop,algorithm=dnn,width=545,height=307"
HOUR_IMG = "https://c.ndtvimg.com/2024-06/n7kugs6o_world-motorcycle-day-2024_625x300_21_June_24.jpg?im=FaceCrop,algorithm=dnn,width=545,height=307"


st.markdown("""
<style>
.main {
    padding: 2rem;
}
h1, h2, h3 {
    color: #2C3E50;
}
.card {
    background: rgba(255,255,255,0.9);
    border-radius: 18px;
    padding: 1.2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}
.stButton > button {
    background: linear-gradient(90deg, #1ABC9C, #16A085);
    color: white;
    border-radius: 12px;
    padding: 0.8rem;
    font-size: 16px;
    font-weight: bold;
}
.stButton > button:hover {
    transform: scale(1.02);
}
.back-btn button {
    background: #34495E !important;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =================================================
# LOAD MODELS
# =================================================
@st.cache_resource
def load_day_model():
    model = joblib.load("Randomforest_day_model1.pkl")
    features = joblib.load("Randomforest_features1.pkl")
    return model, features

@st.cache_resource
def load_hour_model():
    model = joblib.load("xgboost_hour_model.pkl")
    features = joblib.load("xgb_hour_features.pkl")
    return model, features

# =================================================
# HEADER
# =================================================
st.title("🚲 RideWise Bike Demand Forecasting System")

# =================================================
# 🏠 HOME DASHBOARD
# =================================================
if st.session_state.page == "home":

    st.markdown("## 📊 Forecast Dashboard")
    st.markdown("Choose a forecast type to continue")

    col1, col2 = st.columns(2)

    with col1:
        st.image(DAY_IMG, width=500)
        if st.button("DAY-WISE FORECAST"):
            st.session_state.page = "day"
            st.rerun()

    with col2:
        st.image(HOUR_IMG, width=500)
        if st.button("HOUR-WISE FORECAST"):
            st.session_state.page = "hour"
            st.rerun()


    # st.markdown("---")
    # st.markdown("""
    # ### 🚀 About RideWise
    # **RideWise** is an AI-powered system that predicts **bike demand**
    # using weather, time, and calendar features to help
    # bike-sharing services make data-driven decisions.
    # """)
    st.markdown("---")
    st.markdown("""
    ##  About RideWise

    **RideWise** is an AI-powered **Bike Demand Forecasting System** designed to help
    bike-sharing platforms make **smart, data-driven decisions**.

    The system leverages **Machine Learning models** to predict bike demand at both
    **daily** and **hourly** levels by analyzing key influencing factors such as
    weather conditions, time patterns, and calendar information.

    ### 🔍 What RideWise Does
    - 📅 **Day-wise Forecasting**  
    Predicts bike demand for the **next 5 days**, helping operators plan fleet
    availability and maintenance schedules.
    
    - 🕒 **Hour-wise Forecasting**  
    Predicts demand for the **next 6 hours**, enabling real-time operational
    decisions during peak and off-peak hours.

    ### 🧠 How It Works
    RideWise uses historical bike usage data combined with:
    - 🌦 Weather features (temperature, humidity, wind speed)
    - 🕰 Time features (hour, weekday, month, season)
    - 📆 Calendar indicators (working day, holiday)

    These features are processed by trained **Machine Learning models**
    (Random Forest & XGBoost) to generate accurate demand predictions.

    ### 🎯 Why RideWise Matters
    - ✔ Improves bike availability during peak hours
    - ✔ Reduces operational costs
    - ✔ Enhances user satisfaction
    - ✔ Supports sustainable urban mobility

    ### 📊 Built With
    - **Python & Machine Learning**
    - **Streamlit** for interactive UI
    - **Scikit-learn & XGBoost** for modeling
    - **Matplotlib** for visualization

    RideWise transforms raw data into **actionable insights**, making
    bike-sharing systems smarter and more efficient.
    """)


# =================================================
# 📅 DAY-WISE FORECAST PAGE
# =================================================
elif st.session_state.page == "day":

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "home"
        st.rerun()

    st.subheader("📅 Day-wise Bike Demand Forecast")

    model, feature_names = load_day_model()

    with st.expander("📥 Enter Day Details", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            day = st.number_input("Day (1–31)", 1, 31, 15)
            season = st.selectbox(
                "Season",
                [1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"
                }[x]
            )
            mnth = st.slider("Month", 1, 12)

        with col2:
            weekday = st.selectbox("Weekday (0=Sunday)", list(range(7)))
            # weathersit = st.selectbox("Weather Condition ", [1, 2, 3, 4])
            weather_map = {
                "Clear": 1,
                "Mist": 2,
                "Light Rain / Snow": 3,
                "Heavy Rain": 4
                    }

            weather_label = st.selectbox(
                    "🌦 Weather Condition",
                    list(weather_map.keys())
                )

            weathersit = weather_map[weather_label]
            # weathersit = st.selectbox(
            #     "🌦 Weather Condition",
            #     [1, 2, 3, 4],
            #     format_func=lambda x: {
            #         1: "Clear",
            #         2: "Mist",
            #         3: "Light Rain / Snow",
            #         4: "Heavy Rain"
            #     }[x]
            # )

            
        windspeed = st.slider("Windspeed", 0.0, 1.0, 0.2)

        temp = st.slider("Temperature", 0.0, 1.0, 0.5)
        atemp = st.slider("Feels Like Temperature", 0.0, 1.0, 0.5)
        hum = st.slider("Humidity", 0.0, 1.0, 0.5)

    input_data = {
        "season": season,
        "mnth": mnth,
        "holiday": 0,
        "weekday": weekday,
        "workingday": 0 if weekday in [0, 6] else 1,
        "weathersit": weathersit,
        "temp": temp,
        "atemp": atemp,
        "hum": hum,
        "windspeed": windspeed
    }

    def predict_next_days(data, start_day, days=5):
        preds, labels = [], []
        base_weekday = data["weekday"]
        d = start_day

        for i in range(days):
            future = data.copy()
            w = (base_weekday + i) % 7
            future["weekday"] = w
            future["workingday"] = 0 if w in [0, 6] else 1

            X = pd.DataFrame([future])[feature_names]
            preds.append(int(model.predict(X)[0]))
            labels.append(f"Day {d}")
            d = d + 1 if d < 31 else 1

        return labels, preds

    if st.button("🔮 Forecast Next 5 Days"):
        with st.spinner("Predicting demand..."):
            days, forecast = predict_next_days(input_data, day)

        st.success("✅ Forecast Generated")

        days_text =["Sunday ","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        text_date = input_data["weekday"]
        ans_day=[days_text[text_date]]
        for i in range(4):
            text_date+=1
            if text_date > 6 :
                text_date=0
            print(text_date)
            ans_day.append(days_text[text_date])
        print(ans_day)
        cols = st.columns(5)
        for i in range(5):
            cols[i].metric(ans_day[i], forecast[i])

        df = pd.DataFrame({
    "Day": days,
        "Bike Demand": forecast
    })

        styled_df = (
            df.style
            .hide(axis="index")
            .set_properties(**{
                "text-align": "center",
                "font-size": "14px"
            })
            .set_table_styles([
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#1f77b4"),
                        ("color", "white"),
                        ("font-weight", "bold"),
                        ("text-align", "center")
                    ]
                },
                {
                    "selector": "tbody tr:nth-child(even)",
                    "props": [("background-color", "#1a1a1a")]
                }
            ])
        )

                # st.table(styled_df)


        # col1, col2, col3 = st.columns([1, 4, 1])
        # with col2:
        #     st.table(styled_df)


        # fig, ax = plt.subplots(figsize=(8,4))
        # ax.plot(days, forecast, marker='o')
        # ax.set_title("5-Day Bike Demand Trend")
        # ax.set_ylabel("Demand")
        # ax.grid(True, linestyle="--", alpha=0.4)
        # st.pyplot(fig)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(days, forecast)
            ax.set_title("Day Wise  Bike Demand")
            ax.set_xlabel("Day")
            ax.set_ylabel("Demand")
            st.pyplot(fig)

# =================================================
# 🕒 HOUR-WISE FORECAST PAGE
# =================================================
elif st.session_state.page == "hour":

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "home"
        st.rerun()

    st.subheader("🕒 Hour-wise Bike Demand Forecast")

    model, feature_names = load_hour_model()

    with st.expander("📥 Enter Hour Details", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            season = st.selectbox("Season", [1, 2, 3, 4])
            mnth = st.slider("Month", 1, 12)
            hr = st.number_input("Current Hour (0–23)", 0, 23, 9)
            holiday = st.selectbox("Holiday", [0, 1])

        with col2:
            weekday = st.selectbox("Weekday", list(range(7)))
            workingday = st.selectbox("Working Day", [0, 1])
            weather_map = {
                "Clear": 1,
                "Mist": 2,
                "Light Rain / Snow": 3,
                "Heavy Rain": 4
                    }

            weather_label = st.selectbox(
                    "🌦 Weather Condition",
                    list(weather_map.keys())
                )

            weathersit = weather_map[weather_label]

        temp = st.slider("Temperature", 0.0, 1.0, 0.5)
        atemp = st.slider("Feels Like Temp", 0.0, 1.0, 0.5)
        hum = st.slider("Humidity", 0.0, 1.0, 0.5)
        windspeed = st.slider("Windspeed", 0.0, 1.0, 0.2)

    base_data = {
        "season": season,
        "yr": 1,
        "mnth": mnth,
        "hr": hr,
        "holiday": holiday,
        "weekday": weekday,
        "workingday": workingday,
        "weathersit": weathersit,
        "temp": temp,
        "atemp": atemp,
        "hum": hum,
        "windspeed": windspeed
    }

    if st.button("🔮 Forecast Next 6 Hours"):
        with st.spinner("Predicting hourly demand..."):
            hours, values = [], []

            for i in range(7):
                future = base_data.copy()
                future["hr"] = (hr + i) % 24
                X = pd.DataFrame([future])[feature_names]
                hours.append(future["hr"])
                values.append(int(model.predict(X)[0]))

        st.success("✅ Hour-wise Forecast Generated")

        cols = st.columns(7)
        for i in range(7):
            cols[i].metric(f"Hour {hours[i]}", values[i])

#         df = pd.DataFrame({
#     "Hour": hours,
#     "Bike Demand": values
# })

#         col1, col2, col3 = st.columns([1, 4, 1])

        # with col2:
        #     st.dataframe(df)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(hours, values)
            ax.set_title("Hourly Bike Demand")
            ax.set_xlabel("Hour")
            ax.set_ylabel("Demand")
            st.pyplot(fig)

# =================================================
# FOOTER
# =================================================
# st.markdown("---")
# st.markdown("👨‍💻 Developed by **Kavi Bharathi** | RideWise ML Project")

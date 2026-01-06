
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

# -------------------------------------------------
# IMAGES
# -------------------------------------------------
BG_IMG = "https://camo.githubusercontent.com/10b2fb1f78b21d014a5ac328cd62cd76785b6a05463b36caa5cccc03499fae39/68747470733a2f2f736f7068696573752e6e65742f77702d636f6e74656e742f75706c6f6164732f323032312f30312f42696b652d53686172696e672d44656d616e642d31313934783530312e6a7067"

DAY_IMG = "https://c.ndtvimg.com/2024-06/n7kugs6o_world-motorcycle-day-2024_625x300_21_June_24.jpg"
HOUR_IMG = DAY_IMG

# -------------------------------------------------
# CSS (BACKGROUND + ABOUT CARD)
# -------------------------------------------------
st.markdown(f"""
<style>

/* ---------- FULL PAGE BACKGROUND ---------- */
.stApp {{
    background-image: linear-gradient(
        rgba(0,0,0,0.55),
        rgba(0,0,0,0.55)
    ), url("{BG_IMG}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* -------- ABOUT SECTION CARD -------- */
.about-card {{
    background: rgba(0, 0, 0, 0.68);
    backdrop-filter: blur(6px);
    padding: 2.2rem;
    border-radius: 20px;
    max-width: 1100px;
    margin: auto;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
}}

/* -------- HEADINGS -------- */
.about-card h2 {{
    color: #FFD166;
    font-weight: 800;
}}

/* -------- PARAGRAPH TEXT -------- */
.about-card p {{
    color: #F1F1F1;
    font-size: 16.5px;
    line-height: 1.75;
}}

/* -------- STRONG -------- */
.about-card strong {{
    color: #4ECDC4;
}}

</style>
""", unsafe_allow_html=True)

# =================================================
# LOAD MODELS
# =================================================
@st.cache_resource
def load_day_model():
    return joblib.load("Models/Randomforest_day_model1.pkl"), joblib.load("Models/Randomforest_features1.pkl")

@st.cache_resource
def load_hour_model():
    return joblib.load("Models/xgboost_hour_model.pkl"), joblib.load("Models/xgb_hour_features.pkl")

# =================================================
# HEADER
# =================================================
st.title("🚲 RideWise Bike Demand Forecasting System")

# =================================================
# HOME PAGE
# =================================================
if st.session_state.page == "home":

    st.markdown("## 📊 Forecast Dashboard")
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

    st.markdown("---")

    # ---------- ABOUT SECTION (WRAPPED) ----------
    st.markdown("""
    <div class="about-card">
    <h2>🚲 About RideWise</h2>

    <p><strong>RideWise</strong> is an intelligent, AI-powered Bike Demand Forecasting System designed to help modern bike-sharing platforms make accurate, data-driven operational decisions.</p>

    <p>With the rapid growth of urban mobility and shared transportation services, predicting bike demand efficiently has become essential for ensuring customer satisfaction and reducing operational costs. Traditional demand estimation methods often fail to adapt to weather changes, seasonal variations, holidays, and peak commuting hours.</p>

    <p>RideWise supports <strong>day-wise</strong> and <strong>hour-wise</strong> forecasting. Day-wise forecasting enables long-term planning such as fleet sizing and maintenance scheduling, while hour-wise forecasting supports real-time bike redistribution and peak-hour management.</p>

    <p>The system analyzes weather conditions, time-based attributes, and calendar indicators to capture complex real-world demand patterns. At its core, RideWise uses <strong>Random Forest</strong> and <strong>XGBoost</strong> models trained on historical bike-sharing datasets.</p>

    <p>By improving bike availability, reducing operational costs, and enhancing customer satisfaction, RideWise contributes to sustainable transportation and smart city initiatives.</p>

    </div>
    """, unsafe_allow_html=True)

# =================================================
# DAY & HOUR PAGES
# (UNCHANGED — YOUR EXISTING CODE CONTINUES)
# =================================================

## 🌍 Problem Statement

# Bike-sharing services often face challenges such as:
# - Shortage of bikes during peak hours
# - Excess idle bikes during low-demand periods
# - Inefficient fleet distribution
# - Increased operational and maintenance costs

# Traditional estimation methods fail to adapt to changing conditions like
# weather, holidays, and time-based demand patterns.
# RideWise solves this by leveraging historical data and predictive analytics.

# ---

# ## 🔍 What RideWise Does

# ### 📅 Day-wise Demand Forecasting
# - Predicts bike demand for the **next 5 days**
# - Helps in long-term planning of:
#   - Fleet availability
#   - Maintenance schedules
#   - Workforce allocation

# ### 🕒 Hour-wise Demand Forecasting
# - Predicts bike demand for the **next 6 hours**
# - Enables real-time decision-making during:
#   - Peak hours
#   - Weather changes
#   - Special events and holidays

# ---

# ## 🧠 How RideWise Works

# RideWise analyzes historical bike usage data combined with multiple
# influencing factors:

# ### 📊 Input Features
# - 🌦 **Weather Conditions**
#   - Temperature
#   - Humidity
#   - Wind speed
#   - Weather situation
# - 🕰 **Time-based Features**
#   - Hour of the day
#   - Day of the week
#   - Month
#   - Season
# - 📆 **Calendar Information**
#   - Working day
#   - Holiday indicator

# These features are processed and fed into trained **Machine Learning models**
# to generate accurate demand predictions.

# ---

# ## 🤖 Machine Learning Models Used

# - **Random Forest Regressor**
#   - Handles non-linear relationships
#   - Robust against overfitting
# - **XGBoost Regressor**
#   - High performance and accuracy
#   - Efficient handling of large datasets

# The models are trained on historical data and optimized to deliver
# reliable forecasts under varying conditions.

# ---

# ## 🎯 Why RideWise Matters

# RideWise provides tangible benefits to bike-sharing platforms:

# - ✔ Improves bike availability during peak demand
# - ✔ Reduces operational and redistribution costs
# - ✔ Enhances customer satisfaction
# - ✔ Supports smart city initiatives
# - ✔ Promotes sustainable and eco-friendly transportation

# ---

# ## 📊 Technology Stack

# - **Python** for backend logic
# - **Machine Learning** for predictive modeling
# - **Streamlit** for interactive and user-friendly UI
# - **Scikit-learn & XGBoost** for model development
# - **Matplotlib** for visualizations
# - **Joblib** for model persistence

# ---

# ## 🚀 Conclusion

# RideWise transforms raw historical data into **actionable insights**,
# empowering bike-sharing systems to operate more efficiently and intelligently.

# By combining data science, machine learning, and an intuitive interface,
# RideWise contributes to **smarter urban mobility solutions**.
# """)



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

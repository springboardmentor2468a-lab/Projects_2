import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from datetime import datetime, timedelta

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Bike Demand Forecast",
    page_icon="🚲",
    layout="wide"
)

# --------------------------------------------------
# CSS Styling
# --------------------------------------------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background:
        linear-gradient(rgba(248,250,252,0.96), rgba(248,250,252,0.96)),
        url("https://images.unsplash.com/photo-1508973379-df8a68cddac4");
    background-size: cover;
    background-position: center;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #020617);
}
section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

/* Text */
h1, h2, h3, h4, p {
    color: #0f172a !important;
}

/* KPI Cards */
.metric-box {
    background: linear-gradient(135deg, #ffffff, #f1f5f9);
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 12px 25px rgba(0,0,0,0.08);
    text-align: center;
}

/* Content Card */
.card {
    background: white;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 12px 25px rgba(0,0,0,0.08);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Models
# --------------------------------------------------
@st.cache_resource
def load_models():
    try:
        # Assuming you have an hourly model and a daily model
        return joblib.load("hourly_model.pkl"), joblib.load("daily_model.pkl")
    except FileNotFoundError:
        st.error("Model files not found. Please ensure 'hourly_model.pkl' and 'daily_model.pkl' are in the directory.")
        return None, None

hourly_model, daily_model = load_models()


# --------------------------------------------------
# Define Feature Names for Models
# IMPORTANT: These lists must exactly match the features your models were trained on,
# and in the correct order.
# Based on the error message, 'hr', 'holiday', 'weekday', 'workingday', 'weathersit' order was different for hourly
HOURLY_FEATURES = [
    "season", "mnth", "hr", "holiday", "weekday", "workingday",
    "weathersit", "temp", "atemp", "hum", "windspeed"
]

# Based on the error message, daily model requires lag features
DAILY_FEATURES = ['season', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp',
 'atemp', 'hum', 'windspeed', 'cnt_lag1', 'cnt_lag7', 'rolling_mean_7',
 'rolling_std_7']
# --------------------------------------------------


# --------------------------------------------------
# Sidebar Controls
# --------------------------------------------------
st.sidebar.title("🚲 Bike Forecast")

forecast_type = st.sidebar.radio(
    "Prediction Mode",
    ["Daily Forecast", "Hourly Forecast"]
)

if forecast_type == "Hourly Forecast":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Current Conditions")
    current_date = st.sidebar.date_input("Date", datetime.now().date())
    current_time_str = st.sidebar.text_input("Current Hour (0-23)", str(datetime.now().hour))
    try:
        current_hour = int(current_time_str)
        if not (0 <= current_hour <= 23):
            st.sidebar.error("Hour must be between 0 and 23.")
            current_hour = datetime.now().hour # Default to current hour on error
    except ValueError:
        st.sidebar.error("Invalid hour. Please enter a number between 0 and 23.")
        current_hour = datetime.now().hour # Default to current hour on error

else: # Daily Forecast
    st.sidebar.markdown("---")
    st.sidebar.subheader("Starting Conditions")
    current_date = st.sidebar.date_input("Start Date", datetime.now().date())

# Common weather parameters
season = st.sidebar.selectbox("Season", ["Winter", "Spring", "Summer", "Fall"])
weather = st.sidebar.selectbox(
    "Weather",
    ["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow"]
)
temp = st.sidebar.slider("Temperature (°C)", -5, 40, 16)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, 60)
windspeed = st.sidebar.slider("Wind Speed (km/h)", 0, 60, 10)
holiday = st.sidebar.toggle("Holiday")
# NOTE: workingday will be calculated dynamically for daily forecast based on weekday
# For hourly, we assume it's set for the starting day
workingday_initial = st.sidebar.toggle("Working Day", value=True)


run = st.sidebar.button("▶ Run Prediction")

# --------------------------------------------------
# Encoding Functions
# --------------------------------------------------
def get_season(date_obj):
    month = date_obj.month
    if 3 <= month <= 5:
        return 1  # Spring
    elif 6 <= month <= 8:
        return 2  # Summer
    elif 9 <= month <= 11:
        return 3  # Fall
    else:
        return 4  # Winter

def get_weekday(date_obj):
    return date_obj.weekday() # Monday=0, Sunday=6

season_map = {"Winter": 4, "Spring": 1, "Summer": 2, "Fall": 3}
weather_map = {"Clear": 1, "Mist/Cloudy": 2, "Light Rain/Snow": 3, "Heavy Rain/Snow": 4}

# --------------------------------------------------
# Prediction Logic
# --------------------------------------------------
# This function generates the base input for features that don't depend on lags
def get_base_input(date_obj, hour=None, current_holiday_status=False, current_workingday_status=False):
    base_dict = {
        "season": get_season(date_obj),
        "mnth": date_obj.month,
        "weekday": get_weekday(date_obj),
        "weathersit": weather_map[weather],
        "temp": temp,
        "atemp": temp, # Assuming atemp is same as temp for simplicity
        "hum": humidity,
        "windspeed": windspeed,
        "holiday": int(current_holiday_status),
        "workingday": int(current_workingday_status)
    }
    if hour is not None:
        base_dict["hr"] = hour
    return base_dict

# --------------------------------------------------
# Main Layout
# --------------------------------------------------

# === LOAD LOCAL IMAGE ===
# Ensure your image file is named "image.png" and sits next to this script
st.image("image.png", use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True) 

col1, col2, col3 = st.columns(3)

if run:
    if hourly_model is None or daily_model is None:
        st.error("Model files not found. Please ensure .pkl files are in the directory and are valid models.")
    else:
        if forecast_type == "Daily Forecast":
            daily_preds_list = []
            dates_list = []

            # --- IMPORTANT ---
            # Initialize history for daily forecast.
            # In a real application, you would load the *actual* last 7 days of bike counts
            # prior to `current_date` from your database or historical data.
            # For demonstration, we use a placeholder. Adjust these values as needed.
            # If your model needs a history of specific values (e.g., from a test set),
            # make sure this history matches that.
            cnt_history = [500, 550, 600, 620, 580, 650, 700] # Placeholder for 7 previous daily counts

            for i in range(6): # Predict for next 6 days
                future_date = current_date + timedelta(days=i)
                
                # Determine holiday and workingday status for the future date
                is_future_holiday = holiday # Use sidebar holiday status for all 6 days, or implement dynamic lookup
                future_weekday = get_weekday(future_date)
                is_future_workingday = int(future_weekday not in [5, 6] and not is_future_holiday) # 5=Sat, 6=Sun

                # Get base features for the current future date
                base_daily_features = get_base_input(
                    future_date,
                    current_holiday_status=is_future_holiday,
                    current_workingday_status=is_future_workingday
                )
                
                # --- Calculate Lag Features for the current prediction day ---
                lag_features = {
                    'cnt_lag1': cnt_history[-1],
                    'cnt_lag7': cnt_history[0],
                    'rolling_mean_7': np.mean(cnt_history),
                    'rolling_std_7': np.std(cnt_history) if len(cnt_history) > 1 else 0 # Avoid std of single element
                }

                # Combine all features for the current day's prediction
                daily_input_data = {**base_daily_features, **lag_features}
                
                # Create DataFrame using explicit feature names and correct order
                daily_df = pd.DataFrame([daily_input_data], columns=DAILY_FEATURES)
                daily_pred = int(daily_model.predict(daily_df)[0])
                daily_preds_list.append(daily_pred)
                dates_list.append(future_date.strftime("%Y-%m-%d"))

                # Update history for the next iteration by adding the predicted value
                cnt_history.append(daily_pred)
                cnt_history.pop(0) # Remove the oldest entry to maintain 7 days history


            avg_daily_pred = int(np.mean(daily_preds_list))
            peak_day_index = np.argmax(daily_preds_list)
            peak_day = dates_list[peak_day_index]

            with col1:
                st.markdown(f"""
                <div class="metric-box">
                    <h4>🚲 Avg. Daily Rentals (Next 6 Days)</h4>
                    <h2>{avg_daily_pred:,}</h2>
                    <p>Estimated per day</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <h4>🌡 Temperature</h4>
                    <h2>{temp}°C</h2>
                    <p>Demand sensitivity</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-box">
                    <h4>🗓 Peak Day</h4>
                    <h2>{peak_day}</h2>
                    <p>Highest usage</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Daily Demand Trend (Next 6 Days)")
            df_plot = pd.DataFrame({
                "Date": dates_list,
                "Predicted Rentals": daily_preds_list
            })
            fig = px.line(
                df_plot, x="Date", y="Predicted Rentals",
                markers=True, template="plotly_white",
                # ADDED/MODIFIED GRAPH LABELS AND TITLE HERE
                title="Predicted Daily Bike Rentals for the Next 6 Days",
                labels={"Date": "Forecast Date", "Predicted Rentals": "Estimated Bike Rentals"}
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        else: # Hourly Forecast
            hourly_preds_list = []
            hours_list = []
            for i in range(6): # Predict for next 6 hours
                future_hour = (current_hour + i) % 24
                
                # Get base features for the current future hour
                hourly_input_data = get_base_input(
                    current_date, # Date remains constant for 6 hours
                    hour=future_hour,
                    current_holiday_status=holiday,
                    current_workingday_status=workingday_initial # Use sidebar workingday for hourly
                )
                
                # Create DataFrame using explicit feature names and correct order
                hourly_df = pd.DataFrame([hourly_input_data], columns=HOURLY_FEATURES)
                hourly_pred = int(hourly_model.predict(hourly_df)[0])
                hourly_preds_list.append(hourly_pred)
                hours_list.append(f"{future_hour:02d}:00") # Format hour nicely

            avg_hourly_pred = int(np.mean(hourly_preds_list))
            peak_hour_index = np.argmax(hourly_preds_list)
            peak_hour = hours_list[peak_hour_index]

            with col1:
                st.markdown(f"""
                <div class="metric-box">
                    <h4>🚲 Avg. Hourly Rentals (Next 6 Hours)</h4>
                    <h2>{avg_hourly_pred:,}</h2>
                    <p>Estimated per hour</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <h4>🌡 Temperature</h4>
                    <h2>{temp}°C</h4>
                    <p>Demand sensitivity</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-box">
                    <h4>⏰ Peak Hour</h4>
                    <h2>{peak_hour}</h2>
                    <p>Highest usage</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Hourly Demand Trend (Next 6 Hours)")
            df_plot = pd.DataFrame({
                "Hour": hours_list,
                "Predicted Rentals": hourly_preds_list
            })
            fig = px.bar(
                df_plot, x="Hour", y="Predicted Rentals",
                template="plotly_white",
                hover_data={"Hour": True, "Predicted Rentals": True},
                # ADDED/MODIFIED GRAPH LABELS AND TITLE HERE
                title="Predicted Hourly Bike Rentals for the Next 6 Hours",
                labels={"Hour": "Forecast Hour", "Predicted Rentals": "Estimated Bike Rentals"}
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("👈 Select parameters and click **Run Prediction**")
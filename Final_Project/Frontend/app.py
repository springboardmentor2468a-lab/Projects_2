import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib
import base64

# Function to convert image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your logo in Colab



# Path to your background image in Colab
bg_image_path = "/content/Background.png"
bg_image_base64 = get_base64_of_bin_file(bg_image_path)

# Path to the layout image for the welcome page
# Note: This is commented out as per the new instructions to not directly embed layout.jpeg
# layout_path = "/content/layout.jpeg"
# layout_base64 = get_base64_of_bin_file(layout_path)

# ---------------- LOAD FILES ----------------
features = joblib.load("day_features.pkl")

day_model = joblib.load("day_model.pkl")
day_scaler = joblib.load("day_scaler.pkl")

hour_model = joblib.load("hour_model.pkl")
hour_scaler = joblib.load("hour_scaler.pkl")

# Mappings for categorical features
season_map = {
    "Springer": 1,
    "Summer": 2,
    "Fall": 3,
    "Winter": 4
}
weathersit_map = {
    "Clear": 1,
    "Cloudy": 2,
    "Light Snow": 3,
    "Heavy Rain": 4
}

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RideWise – Bike Rental Prediction",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# ---------------- CUSTOM CSS ----------------
st.markdown(f"""
<style>
#MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
            /* This part removes the top padding so your content moves up */
            .block-container {{
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }}
.stApp, body {{
    background-color: #000000;
    background-image: url("data:image/png;base64,{bg_image_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 1rem;
}}

/* Ensure the block containing the main titles is transparent */
div[data-testid="stAppViewContainer"] > section > div[data-testid="stVerticalBlock"] > div[data-testid="stBlock"] {{
    background-color: transparent;
}}

/* Ensure Streamlit columns have no default container-like styling */
div[data-testid="stColumn"] > div:first-child {{
    background-color: transparent !important;
    padding: 0 !important;
    border-radius: 0 !important;
    height: auto !important;
    overflow-y: unset !important;
}}

h2, h4, h5, h6, label, p, span {{
    color: rgba(100, 100, 100, 1) !important;;

}}
h1,h3,h2,h4{{
  text-align: center;
  color: rgba(100, 100, 100, 1) !important; /* Adjusted to an even darker white */
}}


.stRadio label {{
    color: rgba(255, 255, 255, 0.7) !important;
}}

/* Custom styling for DataFrames */
div[data-testid="stDataFrame"] {{
    background-color: rgba(55, 55, 69, 0.7) !important; /* Transparent DataFrames */
    color: rgba(255, 255, 255, 0.7) !important;
}}
div[data-testid="stDataFrame"] * {{
    color: rgba(255, 255, 255, 0.7) !important; /* Ensure all text inside DataFrame is white */
}}
div[data-testid="stDataFrame"] thead th {{
    background-color: rgba(44, 44, 54, 0.7) !important; /* Slightly darker header */
    color: rgba(255, 255, 255, 0.7) !important;
}}
div[data-testid="stDataFrame"] tbody tr:nth-child(even) {{
    background-color: rgba(62, 62, 74, 0.7) !important; /* Alternate row color */
}}
div[data-testid="stDataFrame"] tbody tr:nth-child(odd) {{
    background-color: rgba(55, 55, 69, 0.7) !important; /* Match panel background */
}}

/* Custom styling for transparent selectbox */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div[role="button"] {{
    background-color: transparent !important;
    color: rgba(255, 255, 255, 0.7) !important; /* Ensure text is white */
    border-color: rgba(255, 255, 255, 0.3) !important; /* Subtle white border */
}}
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div[role="button"]:hover {{
    background-color: rgba(255, 255, 255, 0.1) !important; /* Slight hover effect */
}}

/* For the dropdown options themselves */
div[data-testid="stVirtualDropdown"] > div > div {{
    background-color: rgba(55, 55, 69, 0.7) !important; /* Match panel background for options */
    color: rgba(255, 255, 255, 0.7) !important;
}}
div[data-testid="stVirtualDropdown"] > div > div:hover {{
    background-color: rgba(74, 74, 90, 0.7) !important; /* Slightly lighter hover for options */
    color: rgba(255, 255, 255, 0.7) !important;
}}

/* Custom styling for buttons (now black) */
div[data-testid^="stButton"] > button {{
    background-color: #000000 !important; /* Black background */
    border: 1px solid white !important; /* White border */
}}
div[data-testid^="stButton"] > button * {{
    color: rgba(255, 255, 255, 0.7) !important; /* Ensure all text inside the button is white */
}}
div[data-testid^="stButton"] > button:hover {{
    background-color: #333333 !important; /* Slightly lighter black on hover */
    border-color: white !important;
}}
div[data-testid^="stButton"] > button:active {{
    background-color: #555555 !important; /* Even lighter black on active */
    border-color: white !important;
}}
.stApp {{
        background-image: url("data:image/png;base64,{bg_image_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Global Header Color: Darker White */
    h1, h2, h3, h4 {{
        text-align: center;
        color: rgba(100, 100, 100, 1) !important;
    }}

    /* Hero Title: Kept Bright for readability */
    .hero-title {{
        font-size: 60px !important;
        font-weight: 800 !important;
        line-height: 1.1;
        color: white !important;
        text-align: left !important;
        margin-bottom: 10px;
    }}

    /* Right-aligned Glass Container */
    .glass-card {{
        background: rgba(255, 255, 255, 0.1); /* Reverted to more transparent look */
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        color: white; /* Ensure text color is white by default for card */
        width: 280px;
        margin-left: auto; /* Displaces to right end */
        margin-right: 0px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }}

    /* Ensure h1 and h2 inside glass cards are white */
    .glass-card h1,
    .glass-card h2 {{
        color: white !important;
    }}

    /* Neon Green Button */
    div.stButton > button {{
        background-color: #39FF14 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        padding: 12px 40px !important;
        border: none !important;
        margin-top: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# --- PAGE LOGIC ---
if st.session_state.page == 'welcome':


    # Spacing for Hero section
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Layout [Left Content, Middle Spacer, Right Cards]
    col_left, col_mid, col_right = st.columns([4.5, 1.5, 3])

    with col_left:
        st.markdown("""
            <h1 class="hero-title">Predict Tomorrow's<br>Bike Demand<br>Before the City<br>Wakes Up</h1>
            <p style="color: rgba(255,255,255,0.7); font-size: 20px; text-align: left;">
                AI-powered hourly & daily forecasting system.
            </p>
        """, unsafe_allow_html=True)

        if st.button("Try Live Prediction"):
            st.session_state.page = 'prediction'
            st.rerun()

    with col_right:
        # Transparent Containers at the far right
        st.markdown("""
            <div class="glass-card">
                <p style="margin:0; font-size:12px; color:white;">📊 Predicted Demand</p>
                <h1 style="margin:0; font-size:48px; color:white; text-align:left;">412</h1>
                <p style="margin:0; color:#39FF14; font-size:12px;">📈 Weather Impact: +12%</p>
            </div>
            <div style="height: 20px;"></div>
            <div class="glass-card">
                <p style="margin:0; font-size:12px; color:white;">⏰ Peak Hour</p>
                <h2 style="margin:0; color:white; text-align:left;">8:00 AM</h2>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == 'prediction':
    # Inject CSS for prediction page columns specifically
    st.markdown("""
    <style>
    /* Specific styling for left column on prediction page */
    div[data-testid="stColumn"]:first-child > div:first-child {{
        background-color: rgba(55, 55, 69, 0.7) !important;
        padding: 35px !important; /* Increased padding */
        border-radius: 15px !important;
        height: 500px !important; /* Fixed height for the left panel */
        overflow-y: unset !important;
    }}
    /* Specific styling for right column on prediction page */
    div[data-testid="stColumn"]:last-child > div:first-child {{
        background-color: rgba(55, 55, 69, 0.7) !important;
        padding: 40px !important; /* Increased padding */
        border-radius: 15px !important;
        height: 500px !important; /* Fixed height for the right panel */
        overflow-y: auto !important; /* Make right panel scrollable */
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <h1 style="margin: 0;">RideWise</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h3>Bike Rental Prediction System</h3>", unsafe_allow_html=True)

    # ---------------- MAIN LAYOUT ----------------
    left_col, right_col = st.columns([1, 3])

    # ================= LEFT PANEL =================
    with left_col:
        # Content directly inside the Streamlit column, styled via CSS targeting data-testid
        st.markdown("<h2>Prediction Type</h2>", unsafe_allow_html=True)
        mode = st.radio(
            "",
            ["📅 Day-wise Prediction", "⏰ Hour-wise Prediction"]
        )

        # Moved st.info messages to the left panel, conditioned on mode selection
        if mode == "📅 Day-wise Prediction":
            st.info(
                "📅 **Day-wise Prediction** estimates the **total bike rentals for a full day**.\n\n"
                "🔹 Based on season, weather, and calendar factors\n"
                "🔹 Forecasts rentals for **today and the next 6 days**\n\n"
                "👉 Adjust inputs and click **Predict Day Rentals**"
            )
        else:
            st.info(
                "⏰ **Hour-wise Prediction** estimates **bike rentals for specific hours**.\n\n"
                "🔹 Based on hour of day, season, weather, and calendar factors\n"
                "🔹 Forecasts rentals for **current hour and the next 6 hours**\n\n"
                "👉 Adjust inputs and click **Predict Hour Rentals**"
            )

    # ================= RIGHT PANEL =================
    with right_col:
        # Content directly inside the Streamlit column, styled via CSS targeting data-testid

        # ================= DAY PREDICTION =================
        if mode == "📅 Day-wise Prediction":

            st.subheader("📅 Day-wise Rental Prediction")

            col1, col2 = st.columns(2)

            with col1:
                selected_season = st.selectbox("Season", list(season_map.keys()))
                mnth = st.slider("Month", 1, 12)
                holiday = st.checkbox("Holiday")
                weekday = st.slider("Weekday (0=Sun)", 0, 6)
                workingday = st.checkbox("Working Day")

            with col2:
                selected_weathersit = st.selectbox("Weather Situation", list(weathersit_map.keys()))
                temp = st.slider("Temperature (Normalized)", 0.0, 1.0)
                atemp = st.slider("Feels Like Temp (Normalized)", 0.0, 1.0)
                hum = st.slider("Humidity (Normalized)", 0.0, 1.0)
                windspeed = st.slider("Windspeed (Normalized)", 0.0, 1.0)

            day_input_data = {
                "season": season_map[selected_season],
                "mnth": mnth,
                "holiday": int(holiday),
                "weekday": weekday,
                "workingday": int(workingday),
                "weathersit": weathersit_map[selected_weathersit],
                "temp": temp,
                "atemp": atemp,
                "hum": hum,
                "windspeed": windspeed
            }

            day_input = pd.DataFrame([day_input_data])[features]

            if st.button("🚀 Predict Day Rentals"):
                scaled = day_scaler.transform(day_input)
                log_pred = day_model.predict(scaled)[0]
                current_pred = int(np.expm1(log_pred))

                future_inputs, labels = [], []
                for i in range(7):
                    temp_dict = day_input_data.copy()
                    wd = (weekday + i) % 7
                    temp_dict["weekday"] = wd
                    temp_dict["workingday"] = 1 if wd < 5 else 0
                    future_inputs.append(temp_dict)
                    labels.append(f"Day {i}")

                future_df = pd.DataFrame(future_inputs)[features]
                preds = np.expm1(day_model.predict(day_scaler.transform(future_df)))

                st.success(f"Current Day Prediction: {current_pred}")

                result_df = pd.DataFrame({
                    "Day": labels,
                    "Predicted Rentals": preds.astype(int)
                })

                st.dataframe(result_df)

                fig, ax = plt.subplots(figsize=(7, 3.5), facecolor=(0.216, 0.216, 0.271, 0.7)) # Reduced figure size & set facecolor
                ax.bar(result_df["Day"], result_df["Predicted Rentals"], color='#6fa8dc') # Changed bar color
                ax.set_ylabel("Rental Count", color='white', fontsize=10)
                ax.set_title("Next 7 Days Rental Prediction", color='white', fontsize=12)
                ax.set_facecolor((0.216, 0.216, 0.271, 0.7)) # Match panel background
                ax.spines['top'].set_visible(False) # Clean up plot aesthetics
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_edgecolor('white') # Set left spine color
                ax.spines['bottom'].set_edgecolor('white') # Set bottom spine color
                ax.tick_params(axis='x', rotation=45, labelcolor='white') # Ensure labels are white
                ax.tick_params(axis='y', labelcolor='white')
                ax.yaxis.label.set_color('white')
                ax.xaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.grid(axis='y', linestyle='--', alpha=0.3) # Add light grid

                # Add value labels on top of bars, increased fontsize
                max_val_day = result_df["Predicted Rentals"].max()
                for index, value in enumerate(result_df["Predicted Rentals"]):
                    ax.text(index, value + max_val_day * 0.05, str(value), ha='center', va='bottom', color='white', fontsize=10) # Increased fontsize
                ax.set_ylim(0, max_val_day * 1.15) # Adjust y-axis limit for annotations

                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig) # Close the figure to prevent display issues



        # ================= HOUR PREDICTION =================
        else:

            st.subheader("⏰ Hour-wise Rental Prediction")

            col1, col2 = st.columns(2)

            with col1:
                selected_season = st.selectbox("Season", list(season_map.keys()))
                mnth = st.slider("Month", 1, 12)
                hr = st.slider("Hour", 0, 23)
                holiday = st.checkbox("Holiday")
                weekday = st.slider("Weekday (0=Sun)", 0, 6)

            with col2:
                workingday = st.checkbox("Working Day")
                selected_weathersit = st.selectbox("Weather Situation", list(weathersit_map.keys()))
                temp = st.slider("Temperature (Normalized)", 0.0, 1.0)
                atemp = st.slider("Feels Like Temp (Normalized)", 0.0, 1.0)
                hum = st.slider("Humidity (Normalized)", 0.0, 1.0)
                windspeed = st.slider("Windspeed (Normalized)", 0.0, 1.0)

            base_input = {
                "season": season_map[selected_season],
                "mnth": mnth,
                "hr": hr,
                "holiday": int(holiday),
                "weekday": weekday,
                "workingday": int(workingday),
                "weathersit": weathersit_map[selected_weathersit],
                "temp": temp,
                "atemp": atemp,
                "hum": hum,
                "windspeed": windspeed
            }

            if st.button("🚀 Predict Hour Rentals"):
                future_inputs, labels = [], []

                for i in range(7):
                    temp = base_input.copy()
                    new_hr = (hr + i) % 24
                    day_shift = (hr + i) // 24
                    new_weekday = (weekday + day_shift) % 7

                    temp["hr"] = new_hr
                    temp["weekday"] = new_weekday
                    temp["workingday"] = 1 if new_weekday < 5 else 0

                    future_inputs.append(temp)
                    labels.append(f"Hour {new_hr}")

                future_df = pd.DataFrame(future_inputs)
                preds = hour_model.predict(future_df)
                preds = np.maximum(preds, 0)
                st.success(f"Current Hour Prediction: {int(preds[0])}")

                result_df = pd.DataFrame({
                    "Hour": labels,
                    "Predicted Rentals": preds.astype(int)
                })

                st.dataframe(result_df)

                fig, ax = plt.subplots(figsize=(7, 3.5), facecolor=(0.216, 0.216, 0.271, 0.7)) # Reduced figure size & set facecolor
                ax.bar(result_df["Hour"], result_df["Predicted Rentals"], color='#6fa8dc') # Changed bar color
                ax.set_ylabel("Rental Count", color='white', fontsize=10)
                ax.set_title("Next 6 Hours Rental Prediction", color='white', fontsize=12)
                ax.set_facecolor((0.216, 0.216, 0.271, 0.7)) # Match panel background
                ax.spines['top'].set_visible(False) # Clean up plot aesthetics
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_edgecolor('white') # Set left spine color
                ax.spines['bottom'].set_edgecolor('white') # Set bottom spine color
                ax.tick_params(axis='x', rotation=30, labelcolor='white') # Ensure labels are white
                ax.tick_params(axis='y', labelcolor='white')
                ax.yaxis.label.set_color('white')
                ax.xaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.grid(axis='y', linestyle='--', alpha=0.3) # Add light grid

                # Add value labels on top of bars, increased fontsize
                max_val_hour = result_df["Predicted Rentals"].max()
                for index, value in enumerate(result_df["Predicted Rentals"]):
                    ax.text(index, value + max_val_hour * 0.05, str(value), ha='center', va='bottom', color='white', fontsize=10) # Increased fontsize
                ax.set_ylim(0, max_val_hour * 1.15) # Adjust y-axis limit for annotations

                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

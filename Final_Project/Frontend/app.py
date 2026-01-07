import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Urban Bike Demand Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- BACKGROUND IMAGE URLS --------------------
HERO_BG_URL = "https://img.freepik.com/premium-photo/silver-bicycle-sits-against-white-wall_14117-1193307.jpg?semt=ais_hybrid&w=740&q=80"
DASHBOARD_BG_URL = "https://www.shutterstock.com/image-illustration/white-bicycle-on-soft-gray-260nw-2292678519.jpg"

# -------------------- SESSION STATE --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------- BACKGROUND IMAGE FUNCTION --------------------
def set_bg(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------- LOGIN PAGE --------------------
def login_page():
    set_bg(HERO_BG_URL)

    # ---- LOGIN CSS (COMPACT INPUTS) ----
    st.markdown(
        """
        <style>
        .login-box {
            max-width: 30px;
            margin: auto;
            padding-top: 18px;
            text-align: center;
        }

        .login-box input {
            height: 28px !important;
            font-size: 12px !important;
            padding: 4px 8px !important;
            width: 20px !important;
            margin-bottom: 6px !important;
        }

        .login-box label {
            font-size: 13px !important;
        }

        .login-box button {
            width: 22px !important;
            height: 3px !important;
            font-size: 13px !important;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.title("Unlock the Power of")
    st.markdown("## **Urban Analytics**")
    st.markdown("### to Predict Bike Demand")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Get Started"):
        if username and email and password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Please fill all fields")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
def sidebar():
    st.sidebar.title("🚴 Urban Analytics")
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Profile", "Prediction History", "Logout"]
    )
    return page

# -------------------- DASHBOARD PAGE --------------------
def dashboard_page():
    set_bg(DASHBOARD_BG_URL)

    st.markdown("## 🚲 Bike Demand Prediction")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        season = st.selectbox("Season", ["Winter", "Spring", "Summer", "Fall"])
    with col2:
        month = st.selectbox("Month", ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    with col3:
        weekday = st.selectbox("Weekday", ["Sunday", "Monday", "Tuesday",
                                           "Wednesday", "Thursday", "Friday", "Saturday"])
    with col4:
        workingday = st.selectbox("Working Day", ["Yes", "No"])

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        temp = st.number_input("Temperature (°C)", 0, 50, 25)
    with col6:
        feels = st.number_input("Feels Like (°C)", 0, 50, 27)
    with col7:
        humidity = st.number_input("Humidity (%)", 0, 100, 80)
    with col8:
        wind = st.number_input("Wind Speed", 0, 50, 15)

    col9, col10 = st.columns(2)
    with col9:
        weather = st.selectbox("Weather", ["Clear", "Mist", "Rain", "Snow"])
    with col10:
        holiday = st.selectbox("Holiday", ["Yes", "No"])

    if st.button("Predict Demand"):
        prediction = np.random.randint(300, 700)

        st.session_state.history.append({
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Prediction": prediction
        })

        st.success(f"Predicted Bike Demand: {prediction}")

        hours = ["6 AM", "8 AM", "10 AM", "12 PM", "4 PM", "8 PM"]
        values = np.random.randint(200, 700, size=6)

        fig, ax = plt.subplots()
        ax.bar(hours, values)
        ax.set_ylabel("Bike Demand")
        ax.set_title("Hourly Demand Forecast")
        st.pyplot(fig)

# -------------------- PROFILE PAGE --------------------
def profile_page():
    set_bg(DASHBOARD_BG_URL)
    st.markdown("## 👤 Profile")

    st.write("**Username:**", st.session_state.user)
    st.write("**Role:** Analyst")
    st.write("**Project:** Urban Bike Demand Prediction")

# -------------------- HISTORY PAGE --------------------
def history_page():
    set_bg(DASHBOARD_BG_URL)
    st.markdown("## 📊 Prediction History")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.table(df)
    else:
        st.info("No predictions yet.")

# -------------------- LOGOUT --------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.history = []
    st.rerun()

# -------------------- MAIN --------------------
if not st.session_state.logged_in:
    login_page()
else:
    page = sidebar()

    if page == "Dashboard":
        dashboard_page()
    elif page == "Profile":
        profile_page()
    elif page == "Prediction History":
        history_page()
    elif page == "Logout":
        logout()

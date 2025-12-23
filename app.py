import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. PAGE CONFIG & SESSION STATE
# ==========================================
st.set_page_config(page_title="Predicting Bike Sharing Demand", layout="wide")

# Initialize the selection in memory
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = "Home"

# Function to change the page (The "Callback")
def go_to_visuals():
    st.session_state.page_selection = "Visualization"

# ==========================================
# 2. LOAD DATA
# ==========================================
try:
    day_df = pd.read_csv(r"C:\Users\rishy\Desktop\New folder\infosys\day.csv")
    hour_df = pd.read_csv(r"C:\Users\rishy\Downloads\ml\hour.csv")
except FileNotFoundError:
    st.error("CSV files not found. Please check your file paths!")
    st.stop()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
# We link the radio directly to session_state using the 'key'
page = st.sidebar.radio(
    "Navigation", 
    ["Home", "Visualization"], 
    index=0 if st.session_state.page_selection == "Home" else 1,
    key="page_selection" 
)

# ==========================================
# 4. HOME PAGE
# ==========================================
if st.session_state.page_selection == "Home":
    st.title("🚲 Predicting Bike Sharing Demand")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Day-wise Demand Prediction")
        st.markdown("Features Used\n- Season\n- Month\n- Holiday\n- Weather\n- Temp\n- etc.")

    with col2:
        st.subheader("⏰ Hour-wise Demand Prediction")
        st.markdown("Features Used\n- Hour\n- Season\n- Month\n- Weather\n- Humidity\n- etc.")

    st.markdown("---")
    st.info("Click below to view demand analysis")

    # The secret ingredient: 'on_click'
    # This tells Streamlit: "Change the page selection BEFORE you rerun the script"
    st.button("👉 Click Here", on_click=go_to_visuals)

# ==========================================
# 5. VISUALIZATION PAGE
# =============================
if st.session_state.page_selection == "Visualization":
    st.title("📊 Bike Sharing Data Visualization")

    tab1, tab2 = st.tabs(["Day-wise Analysis", "Hour-wise Analysis"])

    with tab1:
        st.subheader("Day-wise Bike Rental Distribution")
        fig1, ax1 = plt.subplots()
        sns.histplot(day_df['cnt'], bins=30, kde=True, ax=ax1)
        
        # --- CHANGE X-AXIS LABELS HERE ---
        # Defining where the ticks should be and what they should say
        ax1.set_xticks([0, 2000, 4000, 6000, 8000])
        ax1.set_xticklabels(["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"])
        
        ax1.set_xlabel("Rental Category")
        st.pyplot(fig1)

    with tab2:
        st.subheader("Hour-wise Bike Rental Distribution")
        fig2, ax2 = plt.subplots()
        sns.histplot(hour_df['cnt'], bins=40, kde=True, color='orange', ax=ax2)
        
        # --- CHANGE X-AXIS LABELS HERE ---
        ax2.set_xticks([0, 200, 400, 600, 800, 1000]) # Adjusted for typical hour counts
        ax2.set_xticklabels(["Day 1", "Day 2", "Day 3", "Day 4", "Day 5","DAY 6 "])
        
        ax2.set_xlabel("Rental Category")
        st.pyplot(fig2)
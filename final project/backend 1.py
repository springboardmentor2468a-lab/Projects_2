import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. LOAD DATA
# ==========================================
@st.cache_data # Adding cache so the app doesn't reload CSV on every click
def load_data():
    try:
        day_df = pd.read_csv(r"C:\Users\rishy\Downloads\ml\day.csv")
        # Convert date column to datetime objects
        day_df['dteday'] = pd.to_datetime(day_df['dteday'])
        return day_df
    except FileNotFoundError:
        st.error("CSV files not found.")
        return pd.DataFrame()

day_df = load_data()

# ==========================================
# 2. SIDEBAR INPUTS & NAVIGATION
# ==========================================
st.sidebar.header("User Inputs")

# Input 1: Date Range Selection
if not day_df.empty:
    min_date = day_df['dteday'].min().to_pydatetime()
    max_date = day_df['dteday'].max().to_pydatetime()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# Input 2: Weather Situation Filter
# (1: Clear, 2: Mist, 3: Light Snow/Rain, 4: Heavy Rain)
weather_choice = st.sidebar.multiselect(
    "Select Weather Situations",
    options=[1, 2, 3, 4],
    default=[1, 2, 3]
)

st.sidebar.markdown("---")

# Navigation
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = "Home"

page = st.sidebar.radio(
    "Navigation", 
    ["Home", "Visualization"], 
    key="main_nav"
)
st.session_state.page_selection = page

# ==========================================
# 3. FILTERING LOGIC
# ==========================================
if not day_df.empty:
    # Filter by Date
    mask = (day_df['dteday'] >= pd.Timestamp(date_range[0])) & (day_df['dteday'] <= pd.Timestamp(date_range[1]))
    filtered_df = day_df.loc[mask]
    
    # Filter by Weather
    filtered_df = filtered_df[filtered_df['weathersit'].isin(weather_choice)]

# ==========================================
# 4. PAGE CONTENT
# ==========================================
if page == "Home":
    st.title("🚲 Predicting Bike Sharing Demand")
    
    if not day_df.empty:
        st.write(f"### Dataset Preview ({len(filtered_df)} records found)")
        st.dataframe(filtered_df.head())
        
        # Simple Metric Cards using inputs
        col1, col2 = st.columns(2)
        col1.metric("Avg Temp", f"{filtered_df['temp'].mean():.2f}")
        col2.metric("Total Bookings", f"{filtered_df['cnt'].sum():,}")
        
    st.info("Adjust the filters in the sidebar to update the data!")
    
    if st.button("👉 View Visualizations"):
        st.session_state.page_selection = "Visualization"
        st.rerun()

if page == "Visualization":
    st.title("📊 Bike Sharing Data Visualization")
    
    if not filtered_df.empty:
        st.subheader("Temperature vs. Total Rides")
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_df, x='temp', y='cnt', hue='weathersit', ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected filters.")
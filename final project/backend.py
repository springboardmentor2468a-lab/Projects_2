import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
# Import from logic script if separated: from logic import load_data, filter_data

# --- CONFIG & DATA INITIALIZATION ---
st.set_page_config(page_title="Bike Sharing Dashboard")

@st.cache_data
def get_cached_data():
    return load_data(r"C:\Users\rishy\Downloads\ml\day.csv")

day_df = get_cached_data()

# --- SIDEBAR: UI INPUTS ---
st.sidebar.header("User Inputs")

if not day_df.empty:
    min_date = day_df['dteday'].min().to_pydatetime()
    max_date = day_df['dteday'].max().to_pydatetime()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    weather_choice = st.sidebar.multiselect(
        "Select Weather Situations",
        options=[1, 2, 3, 4],
        default=[1, 2, 3]
    )

    # CALL BACKEND FILTERING
    filtered_df = filter_data(day_df, date_range, weather_choice)

page = st.sidebar.radio("Navigation", ["Home", "Visualization"])

# --- MAIN CONTENT: UI RENDERING ---
if page == "Home":
    st.title("🚲 Predicting Bike Sharing Demand")
    
    if not day_df.empty:
        st.write(f"### Dataset Preview ({len(filtered_df)} records found)")
        st.dataframe(filtered_df.head())
        
        col1, col2 = st.columns(2)
        col1.metric("Avg Temp", f"{filtered_df['temp'].mean():.2f}")
        col2.metric("Total Bookings", f"{filtered_df['cnt'].sum():,}")
    
    st.info("Adjust filters in the sidebar to update data.")

elif page == "Visualization":
    st.title("📊 Bike Sharing Data Visualization")
    
    if not filtered_df.empty:
        st.subheader("Temperature vs. Total Rides")
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_df, x='temp', y='cnt', hue='weathersit', ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No data available.")
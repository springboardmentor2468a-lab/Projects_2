import pandas as pd

# ==========================================
# BACKEND: DATA & LOGIC
# ==========================================

def load_data(file_path):
    """Handles data loading and initial cleaning."""
    try:
        df = pd.read_csv(file_path)
        df['dteday'] = pd.to_datetime(df['dteday'])
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def filter_data(df, date_range, weather_choice):
    """Handles all filtering logic."""
    if df.empty:
        return df
    
    # Filter by Date
    start_date, end_date = date_range
    mask = (df['dteday'] >= pd.Timestamp(start_date)) & (df['dteday'] <= pd.Timestamp(end_date))
    df = df.loc[mask]
    
    # Filter by Weather
    df = df[df['weathersit'].isin(weather_choice)]
    
    return df
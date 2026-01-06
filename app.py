import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AI RideWise – Bike Demand Forecasting",
    page_icon="🚲",
    layout="wide"
)

# Simple CSS tweaks for a cleaner UI
st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        :root{
            --bg-1: #080812;
            --bg-2: #0f1220;
            --card-bg: rgba(255,255,255,0.04);
            --glass: rgba(255,255,255,0.03);
            --text-light: #e9f1ff;
            --text-dark: #0b1220;
            --muted-light: #9fb1ff;
            --accent: linear-gradient(90deg, #7c97ff, #3dd9eb);
            --neon: #7c97ff;
            --glass-border: rgba(255,255,255,0.06);
        }
        html, body, .stApp {
            height: 100%;
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
            background: radial-gradient(800px 400px at 10% 10%, rgba(124,151,255,0.06), transparent),
                        radial-gradient(600px 300px at 90% 0%, rgba(61,217,235,0.04), transparent),
                        linear-gradient(180deg, var(--bg-1), var(--bg-2));
            color: var(--text-light);
            background-attachment: fixed;
        }
        /* Glass card */
        .card { background: var(--card-bg); padding: 18px; border-radius: 14px; border: 1px solid var(--glass-border); box-shadow: 0 12px 40px rgba(2,6,23,0.6); }
        .title {text-align: center; font-weight:800; color:var(--text-light); margin-bottom:6px}
        .muted {color: rgba(255,255,255,0.7); margin-bottom:12px}
        .stSidebar .block-container { padding-top: 1rem; }
        .metric .value { color: var(--neon) !important; }
        /* Futuristic button */
        .stButton>button {
            background: linear-gradient(90deg, rgba(124,151,255,0.12), rgba(61,217,235,0.06));
            color: var(--text-light);
            border-radius: 10px;
            padding: 0.5rem 1.0rem;
            border: 1px solid rgba(124,151,255,0.16);
            box-shadow: 0 8px 30px rgba(124,151,255,0.06), 0 0 14px rgba(124,151,255,0.04) inset;
            font-weight:700;
        }
        .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 18px 50px rgba(124,151,255,0.12); }
        /* inputs */
        input, .stTextInput, .stNumberInput, .stSelectbox { background: rgba(255,255,255,0.03) !important; color: var(--text-light) !important; border-radius: 10px !important; }
        label, p, div, span, h1, h2, h3, h4, h5, h6 { color: var(--text-light) !important; }
        /* Theme overrides: when class is applied to the <html> element */
        html.theme-light, body.theme-light, html.theme-light .stApp { background: linear-gradient(180deg,#f7fbff,#eaf3ff); color: var(--text-dark); }
        html.theme-light label, html.theme-light p, html.theme-light div, html.theme-light span, html.theme-light h1, html.theme-light h2 { color: var(--text-dark) !important; }
        html.theme-light .card { background: rgba(255,255,255,0.95); border: 1px solid rgba(14,30,37,0.04); box-shadow: 0 8px 30px rgba(2,6,23,0.06); }
        html.theme-dark .stButton>button { color: var(--text-light); }
        .big-metric { font-size: 22px; font-weight:800; }
        .nav-logo { width:100%; border-radius:10px; }
        .muted.small { color: rgba(255,255,255,0.6); font-size:13px; }
        .neon-label { color: var(--neon); font-weight:700; }
        /* subtle animated accent under header */
        .header-accent { height:6px; width:160px; margin: 8px auto 18px; background: linear-gradient(90deg,#5e7cff,#3dd9eb); border-radius:8px; opacity:0.95 }
        /* dashboard card */
        .dash-row{ display:flex; gap:18px; margin-bottom:22px }
        .dash-card{ padding:18px; border-radius:12px; border:1px solid rgba(255,255,255,0.04); background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); box-shadow: 0 16px 40px rgba(2,6,23,0.5); }
        .dash-card h3{ margin:0 0 6px }
        .card-cta{ margin-top:12px; }
        .metric-big .value{ font-size:26px !important; font-weight:800 }
        .sparkline{ height:48px }
+        /* hide Streamlit sidebar (we don't need it) */
+        [data-testid="stSidebar"]{ display:none !important; }
        /* make charts look nicer in cards */
        .stBarChart > div { border-radius: 10px; overflow: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
)

# ==========================================
# SESSION STATE
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "home"
# NOTE: Sidebar removed per user request — theme selector lives in header
# (do not duplicate the selector here to avoid widget key collisions)


# Safe default UI control values (defined globally to avoid NameError)
lag_source = "Use recent lags"
custom_baseline = None
smoothing_cap = 0.5
show_lags = False

# ==========================================
# LOAD MODEL
# ==========================================
@st.cache_resource
def load_model():
    model = joblib.load("bike_demand_pipeline.pkl")
    feature_names = [
        "season","mnth","hr","holiday","weekday","workingday",
        "weathersit","temp","atemp","hum","windspeed"
    ]
    # Try to detect the feature names the model was fitted with.
    expected_features = None
    if hasattr(model, "feature_names_in_"):
        expected_features = list(model.feature_names_in_)
    else:
        # If the pipeline stores the preprocessor with feature metadata, try that too.
        try:
            expected_features = list(model.named_steps["preprocessor"].feature_names_in_)
        except Exception:
            expected_features = None

    return model, feature_names, expected_features

model, feature_names, expected_features = load_model()


# ---------- Time-series helpers (from week5 notebook) ----------
def create_lagged_features(df, target_col='cnt', lags=5):
    df_lagged = df.copy()
    for i in range(1, lags + 1):
        df_lagged[f'lag_{i}'] = df_lagged[target_col].shift(i)
    return df_lagged.dropna()


def multi_step_forecast(model, last_X, steps=5):
    forecasts = []
    # Ensure we pass a DataFrame with expected column names when possible
    try:
        if hasattr(model, 'feature_names_in_') and hasattr(last_X, 'index'):
            current_features = pd.DataFrame([last_X.values], columns=list(last_X.index))
        else:
            current_features = last_X.values.reshape(1, -1).astype(float)
    except Exception:
        current_features = last_X.values.reshape(1, -1).astype(float)

    for _ in range(steps):
        pred = model.predict(current_features)[0]
        forecasts.append(pred)
        current_features = np.roll(current_features, 1)
        current_features[0, 0] = pred

    return forecasts


def shift_lags_and_insert(cur_series, lag_cols, pred):
    cur = cur_series.copy()
    if len(lag_cols) > 0:
        for i in range(len(lag_cols)-1, 0, -1):
            cur[lag_cols[i]] = cur[lag_cols[i-1]]
        cur[lag_cols[0]] = pred
    return cur


@st.cache_resource
def train_day_ts_model():
    model_path = "day_ts_model.pkl"
    if os.path.exists(model_path):
        rf, cols, last_X = joblib.load(model_path)
        return rf, cols, last_X

    dfd = pd.read_csv("day.csv")
    dfd = dfd.drop(columns=['instant', 'dteday', 'yr', 'casual', 'registered'], errors='ignore')
    dfd_ts = create_lagged_features(dfd, target_col='cnt', lags=5)
    X_ts_d = dfd_ts.drop('cnt', axis=1)
    y_ts_d = dfd_ts['cnt']
    split_point = int(len(X_ts_d) * 0.8)
    X_train = X_ts_d.iloc[:split_point]
    y_train = y_ts_d.iloc[:split_point]
    rf = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42)
    rf.fit(X_train, y_train)
    last_X = X_ts_d.iloc[-1]
    cols = list(X_ts_d.columns)
    joblib.dump((rf, cols, last_X), model_path)
    return rf, cols, last_X


@st.cache_resource
def train_hour_ts_model():
    model_path = "hour_ts_model.pkl"
    if os.path.exists(model_path):
        rf, cols, last_X = joblib.load(model_path)
        return rf, cols, last_X

    dfh = pd.read_csv("hour.csv")
    dfh = dfh.drop(columns=['instant', 'dteday', 'yr', 'casual', 'registered'], errors='ignore')
    dfh_ts = create_lagged_features(dfh, target_col='cnt', lags=6)
    X_ts_h = dfh_ts.drop('cnt', axis=1)
    y_ts_h = dfh_ts['cnt']
    split_point = int(len(X_ts_h) * 0.8)
    X_train = X_ts_h.iloc[:split_point]
    y_train = y_ts_h.iloc[:split_point]
    rf = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    last_X = X_ts_h.iloc[-1]
    cols = list(X_ts_h.columns)
    joblib.dump((rf, cols, last_X), model_path)
    return rf, cols, last_X

# ==========================================
# HEADER / HERO (clean, minimal, SaaS-like)
# ==========================================
# Title + compact theme control in the header
with st.container():
    left, right = st.columns([4,1])
    with left:
        st.markdown("<h1 style='margin:0; font-weight:700; font-size:28px;'>AI RideWise</h1>", unsafe_allow_html=True)
        st.markdown("<div class='muted small'>Forecast bike demand using weather and time features</div>", unsafe_allow_html=True)
    with right:
        # Keep a simple manual theme selector (no 'Auto' option)
        theme_choice = st.selectbox("", ["Light", "Dark"], index=1, key="page_theme")
        if theme_choice == "Dark":
            st.markdown("<script>document.documentElement.classList.add('theme-dark');document.documentElement.classList.remove('theme-light');</script>", unsafe_allow_html=True)
        elif theme_choice == "Light":
            st.markdown("<script>document.documentElement.classList.add('theme-light');document.documentElement.classList.remove('theme-dark');</script>", unsafe_allow_html=True)

# navigation helper to reliably change pages then rerun
def navigate(page_name: str):
    st.session_state.page = page_name
    try:
        st.experimental_rerun()
    except Exception:
        # fallback
        st.rerun()

# ==========================================
# HOME PAGE
# ==========================================
if st.session_state.page == "home":

    # Hero accent and subtitle
    st.markdown('<div class="header-accent"></div>', unsafe_allow_html=True)
    st.markdown("<div class='muted small'>Explore forecasts and run predictions</div>", unsafe_allow_html=True)

    # Feature / benefit cards
    with st.container():
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div class='card'><h3 style='margin:0 0 8px;'>Smart Cities</h3><div class='muted small'>Allocate bikes where demand peaks to reduce wait times.</div></div>", unsafe_allow_html=True)
        c2.markdown("<div class='card'><h3 style='margin:0 0 8px;'>Efficiency</h3><div class='muted small'>Lower redistribution costs using accurate signals.</div></div>", unsafe_allow_html=True)
        c3.markdown("<div class='card'><h3 style='margin:0 0 8px;'>Health & Mobility</h3><div class='muted small'>Empower healthier travel choices through reliable availability.</div></div>", unsafe_allow_html=True)

    st.markdown("")

    # Action cards to navigate
    a1, a2 = st.columns(2)
    if a1.button("Open Day forecast"):
        navigate("day")
    if a2.button("Open Hour forecast"):
        navigate("hour")

    st.markdown("---")
    st.markdown("""
    ### About RideWise
    A compact, data-driven forecasting tool for bike-sharing operations.
    """)

# ==========================================
# DAY-WISE FORECAST
# ==========================================
elif st.session_state.page == "day":

    if st.button("⬅ Back to Dashboard"):
        navigate("home")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📅 Day-wise Bike Demand Forecast (Next 5 Days)")

    with st.expander("Enter Inputs", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            season = st.selectbox("Season", [1,2,3,4])
            mnth = st.slider("Month", 1, 12)
            weekday = st.selectbox("Weekday (0=Sunday)", list(range(7)))

        with col2:
            weathersit = st.selectbox("Weather", [1,2,3,4])
            temp = st.slider("Temperature", 0.0, 1.0, 0.5)
            hum = st.slider("Humidity", 0.0, 1.0, 0.5)

        atemp = temp
        windspeed = st.slider("Windspeed", 0.0, 1.0, 0.2)

    # Results card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if st.button("Forecast Next 5 Days"):
        preds, labels = [], []
        base_weekday = weekday

        # Use persisted or trained day time-series model for multi-step forecasting
        rf_day, day_cols, last_X = train_day_ts_model()

        cur = last_X.copy()
        for i in range(5):
            if 'season' in day_cols:
                cur['season'] = season
            if 'mnth' in day_cols:
                cur['mnth'] = mnth
            if 'weekday' in day_cols:
                cur['weekday'] = (base_weekday + i) % 7
            if 'workingday' in day_cols:
                cur['workingday'] = 0 if ((base_weekday + i) % 7) in [0,6] else 1
            if 'weathersit' in day_cols:
                cur['weathersit'] = weathersit
            if 'temp' in day_cols:
                cur['temp'] = temp
            if 'atemp' in day_cols:
                cur['atemp'] = atemp
            if 'hum' in day_cols:
                cur['hum'] = hum
            if 'windspeed' in day_cols:
                cur['windspeed'] = windspeed

            # pass a DataFrame with correct column names to avoid sklearn warnings
            try:
                x_df = pd.DataFrame([cur.values], columns=day_cols)
            except Exception:
                x_df = pd.DataFrame([cur.values])
            f = rf_day.predict(x_df)[0]
            preds.append(int(round(f)))
            labels.append(f"Day {i+1}")

            arr = np.roll(cur.values, 1)
            arr[0] = f
            cur = shift_lags_and_insert(cur, [c for c in day_cols if c.startswith('lag_')], f)

        cols = st.columns(5)
        for i in range(5):
            cols[i].metric(labels[i], preds[i])

        # Streamlit chart (cleaner, responsive)
        st.markdown("## Day-wise Bike Demand")
        st.bar_chart(pd.Series(preds, index=labels))

        # Also display plain-text multi-step forecast like the notebook output
        st.markdown("**--- Day-Wise (Next 5 Days) Forecast ---**")
        for i, p in enumerate(preds, start=1):
            st.markdown(f"Day + {i}: {int(round(p))} bike rentals")
    st.markdown('</div>', unsafe_allow_html=True)

    # Small visualization card for current sample bars
    try:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('### Visualization')
        st.bar_chart(pd.Series(bars, index=labels))
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        pass
        

        # (Removed duplicate hourly lag controls from Day page.)

        # Duplicate day-forecast handler removed — primary forecast button/handler is above the visualization.


    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# HOUR-WISE FORECAST
# ==========================================
elif st.session_state.page == "hour":

    if st.button("⬅ Back to Dashboard"):
        navigate("home")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Hour-wise Bike Demand Forecast (Next 6 Hours)")

    # Ensure lag-control variables exist with safe defaults even if UI widgets
    # are not instantiated in some execution paths.
    lag_source = "Use recent lags"
    custom_baseline = None
    smoothing_cap = 0.5
    show_lags = False

    with st.expander("📥 Enter Inputs", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            season = st.selectbox("Season", [1,2,3,4])
            mnth = st.slider("Month", 1, 12)
            hr = st.number_input("Current Hour", 0, 23, 9)

        with col2:
            weekday = st.selectbox("Weekday", list(range(7)))
            weathersit = st.selectbox("Weather", [1,2,3,4])

        temp = st.slider("Temperature", 0.0, 1.0, 0.5)
        hum = st.slider("Humidity", 0.0, 1.0, 0.5)
        atemp = temp
        windspeed = st.slider("Windspeed", 0.0, 1.0, 0.2)

        # Removed lag-source controls and smoothing slider per UI simplification
        # Use recent lags by default and do not cap hourly change (smoothing_cap=1.0)
        smoothing_cap = 1.0
        show_lags = False
    if st.button("🔮 Forecast Next 6 Hours"):
        hours, values = [], []


        # Train/load hour time-series model and run multi-step forecast using lag features.
        rf_hour, hour_cols, last_X_h = train_hour_ts_model()

        # Build starting vector using recent lags (default behavior)
        cur_h = last_X_h.copy()
        lag_cols = [c for c in hour_cols if c.startswith('lag_')]
        for i in range(6):
            if 'season' in hour_cols:
                cur_h['season'] = season
            if 'mnth' in hour_cols:
                cur_h['mnth'] = mnth
            if 'hr' in hour_cols:
                cur_h['hr'] = (hr + i) % 24
            if 'weekday' in hour_cols:
                cur_h['weekday'] = weekday
            if 'workingday' in hour_cols:
                cur_h['workingday'] = 0 if weekday in [0,6] else 1
            if 'weathersit' in hour_cols:
                cur_h['weathersit'] = weathersit
            if 'temp' in hour_cols:
                cur_h['temp'] = temp
            if 'atemp' in hour_cols:
                cur_h['atemp'] = atemp
            if 'hum' in hour_cols:
                cur_h['hum'] = hum
            if 'windspeed' in hour_cols:
                cur_h['windspeed'] = windspeed

            # pass a DataFrame with correct column names to avoid sklearn warnings
            try:
                x_df = pd.DataFrame([cur_h.values], columns=hour_cols)
            except Exception:
                x_df = pd.DataFrame([cur_h.values])
            f = rf_hour.predict(x_df)[0]

            # smoothing: cap change relative to previous recent value (lag_1)
            prev = float(cur_h[lag_cols[0]]) if len(lag_cols) > 0 else f
            allowed_min = prev * (1 - smoothing_cap)
            allowed_max = prev * (1 + smoothing_cap)
            f = float(max(min(f, allowed_max), allowed_min))

            hours.append((hr + i) % 24)
            values.append(int(round(f)))

            # shift only lag columns and inject the prediction as lag_1
            cur_h = shift_lags_and_insert(cur_h, lag_cols, f)

        cols = st.columns(6)
        for i in range(6):
            cols[i].metric(f"Hour {hours[i]}", values[i])

        st.markdown("## Hourly Bike Demand")
        st.bar_chart(pd.Series(values, index=hours))

        # Plain-text hourly forecast lines
        st.markdown("**--- Hour-Wise (Next 6 Hours) Forecast ---**")
        for i, v in enumerate(values, start=1):
            st.markdown(f"Hour + {i}: {int(round(v))} bike rentals")

    st.markdown('</div>', unsafe_allow_html=True)

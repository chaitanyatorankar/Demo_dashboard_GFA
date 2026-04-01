import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Sense Analytics", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
    url("https://images.unsplash.com/photo-1504384308090-c894fdcc538d");
    background-size: cover;
}
.title {text-align:center;color:white;font-size:50px;font-weight:700;}
.subtitle {text-align:center;color:#bbb;margin-bottom:30px;}
.card {
    background: rgba(255,255,255,0.08);
    padding:25px;border-radius:18px;text-align:center;color:white;
}
.box {
    background: rgba(255,255,255,0.1);
    padding:25px;border-radius:18px;color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"

with col2:
    if st.button("ℹ️ About"):
        st.session_state.page = "about"

with col3:
    if not st.session_state.logged_in:
        if st.button("🔐 Login"):
            st.session_state.page = "login"
    else:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "home"
            st.rerun()

# ---------------- HOME ----------------
if st.session_state.page == "home" and not st.session_state.logged_in:

    st.markdown('<div class="title">🚀 Stock Sense Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart AI-Based Stock Prediction Platform</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card">📊<br><b>Analyze Stocks</b></div>', unsafe_allow_html=True)
    c2.markdown('<div class="card">🔮<br><b>Forecast Prices</b></div>', unsafe_allow_html=True)
    c3.markdown('<div class="card">⚡<br><b>Live Data</b></div>', unsafe_allow_html=True)

    st.stop()

# ---------------- ABOUT ----------------
if st.session_state.page == "about" and not st.session_state.logged_in:

    st.markdown('<div class="title">ℹ️ About</div>', unsafe_allow_html=True)

    st.write("""
    Stock Sense Analytics helps analyze Indian stocks using AI.
    - Live Data
    - ARIMA Forecast
    - Sector Analysis
    """)

    st.stop()

# ---------------- LOGIN ----------------
if st.session_state.page == "login" and not st.session_state.logged_in:

    st.markdown('<div class="title">🔐 Login</div>', unsafe_allow_html=True)

    users = {"admin":"1234", "chaitanya":"finance123"}

    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password").strip()

    st.info("Demo: chaitanya / finance123")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# ---------------- DASHBOARD (ONLY AFTER LOGIN) ----------------
if st.session_state.logged_in:

    st.markdown('<div class="title">📊 Stock Dashboard</div>', unsafe_allow_html=True)

    st.sidebar.header("Settings")

    start_date = st.sidebar.date_input("Start Date", d.date(2022,1,1))
    end_date = st.sidebar.date_input("End Date", d.date.today())

    forecast_days = st.sidebar.slider("Forecast Days", 5, 90, 30)

    sector_stocks = {
        "IT": {"TCS":"TCS.NS","Infosys":"INFY.NS"},
        "Banking": {"HDFC Bank":"HDFCBANK.NS","ICICI":"ICICIBANK.NS"},
        "Auto": {"Tata Motors":"TATAMOTORS.NS","Maruti":"MARUTI.NS"}
    }

    sector = st.sidebar.selectbox("Sector", list(sector_stocks.keys()))
    stock = st.sidebar.selectbox("Stock", list(sector_stocks[sector].keys()))
    symbol = sector_stocks[sector][stock]

    df = yf.download(symbol, start=start_date, end=end_date)

    if not df.empty:
        df = df[['Close']]

        model = ARIMA(df['Close'], order=(5,1,0))
        model_fit = model.fit()

        forecast = model_fit.forecast(steps=forecast_days)

        future_dates = pd.date_range(df.index[-1], periods=forecast_days+1, freq='B')[1:]

        fig, ax = plt.subplots()
        ax.plot(df.index, df['Close'], label="Actual")
        ax.plot(future_dates, forecast, '--', label="Forecast")
        ax.legend()

        st.pyplot(fig)

        st.dataframe(pd.DataFrame({"Forecast": forecast.values}, index=future_dates))

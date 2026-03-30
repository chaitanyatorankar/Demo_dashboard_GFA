import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as d
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="India Finance Analysis - ARIMA Forecast", layout="wide")

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state["start_app"] = False

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- Attractive Background + Center UI ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
    url("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.login-box {
    background-color: rgba(255,255,255,0.1);
    padding: 40px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    width: 350px;
    margin: auto;
    margin-top: 100px;
    text-align: center;
}

.main-title {
    font-size: 48px;
    font-weight: 700;
    text-align: center;
    color: white;
}

.sub-text {
    font-size: 20px;
    text-align: center;
    color: #f1f1f1;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN / SIGNUP
# =========================
if not st.session_state["logged_in"]:

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("## 🔐 Login / Sign Up")

    option = st.radio("", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    users = {
        "admin": "1234",
        "chaitanya": "finance123",
        "demo": "demo123"
    }

    if option == "Login":
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["logged_in"] = True
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    else:
        if st.button("Sign Up"):
            st.success("Account created! (Demo only)")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state["start_app"]:

    st.markdown('<div class="main-title">Groww Your Wealth 📈</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Analyze Indian Stocks & Forecast Trends using ARIMA Model</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("NIFTY 50", "22,300", "-1.2%")
    col2.metric("BANKNIFTY", "48,200", "-0.8%")
    col3.metric("SENSEX", "73,500", "-1.0%")

    if st.button("🚀 Get Started"):
        st.session_state["start_app"] = True
        st.rerun()

    st.stop()

# =========================
# 📊 MAIN DASHBOARD
# =========================

st.title("🇮🇳 India Finance Analysis with ARIMA Forecast")

# Sidebar
st.sidebar.header("⚙️ Customize Analysis")

start_date = st.sidebar.date_input("Start Date", d.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", d.date.today())

forecast_days = st.sidebar.slider("Forecast Days", 5, 60, 10)

# --- Stock Data (25 Companies) ---
sector_stocks = {

    "IT": {
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "Wipro": "WIPRO.NS",
        "HCL Tech": "HCLTECH.NS",
        "Tech Mahindra": "TECHM.NS"
    },

    "Banking": {
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "SBI": "SBIN.NS",
        "Axis Bank": "AXISBANK.NS",
        "Kotak Bank": "KOTAKBANK.NS"
    },

    "FMCG": {
        "HUL": "HINDUNILVR.NS",
        "ITC": "ITC.NS",
        "Nestle": "NESTLEIND.NS",
        "Britannia": "BRITANNIA.NS",
        "Dabur": "DABUR.NS"
    },

    "Energy": {
        "Reliance": "RELIANCE.NS",
        "ONGC": "ONGC.NS",
        "NTPC": "NTPC.NS",
        "Power Grid": "POWERGRID.NS",
        "Coal India": "COALINDIA.NS"
    },

    "Auto": {
        "Maruti": "MARUTI.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "M&M": "M&M.NS",
        "Bajaj Auto": "BAJAJ-AUTO.NS",
        "Hero MotoCorp": "HEROMOTOCO.NS"
    }
}

sector_choice = st.sidebar.selectbox("Select Sector", list(sector_stocks.keys()))
stock_choice = st.sidebar.selectbox(
    "Select Stock",
    sorted(sector_stocks[sector_choice].keys())
)

symbol = sector_stocks[sector_choice][stock_choice]

# --- ARIMA Function ---
def arima_analysis(symbol):
    df = yf.download(symbol, start=start_date, end=end_date)

    if df.empty:
        st.error("No Data Found")
        return None

    df = df[['Close']]
    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=forecast_days)
    future_dates = pd.date_range(df.index[-1], periods=forecast_days+1, freq='B')[1:]

    return df, forecast, future_dates

# --- Run ---
result = arima_analysis(symbol)

if result:
    df, forecast, future_dates = result

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df.index, df['Close'], label="Actual Price")
    ax.plot(future_dates, forecast, linestyle='--', label="Forecast")
    ax.set_title(f"{stock_choice} Price Forecast")
    ax.legend()

    st.pyplot(fig)

    st.subheader("Forecast Data")
    st.dataframe(pd.DataFrame({"Forecast": forecast.values}, index=future_dates))

# --- Logout ---
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["start_app"] = False
    st.rerun()

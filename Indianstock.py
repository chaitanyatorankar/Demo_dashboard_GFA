import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="India Finance Analysis", layout="wide")

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state["start_app"] = False
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
    url("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f");
    background-size: cover;
    background-position: center;
}

/* FIXED CENTER TITLE */
.center-title {
    text-align: center;
    margin-top: 60px;
    margin-bottom: 20px;
    background: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    color: white;
    font-size: 26px;
    font-weight: bold;
    width: 400px;
    margin-left: auto;
    margin-right: auto;
}

/* LOGIN BOX */
.login-box {
    background: rgba(255,255,255,0.1);
    padding: 30px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    width: 400px;
    margin: auto;
    text-align: center;
}

/* CLEAN ERROR MESSAGE */
.error-msg {
    color: #ff4b4b;
    font-size: 14px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN SYSTEM
# =========================
if not st.session_state["logged_in"]:

    st.markdown('<div class="center-title">🇮🇳 Welcome to Indian Stock Analysis</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    option = st.radio("", ["Login", "Sign Up", "Forgot Password"])

    username = st.text_input("Username")

    password = ""
    if option != "Forgot Password":
        password = st.text_input("Password", type="password")

    users = {
        "admin": "1234",
        "chaitanya": "finance123",
        "demo": "demo123"
    }

    error_message = ""

    # LOGIN
    if option == "Login":
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                error_message = "Invalid username or password"

    # SIGN UP
    elif option == "Sign Up":
        if st.button("Create Account"):
            st.success("Account created (Demo Only)")

    # FORGOT PASSWORD
    elif option == "Forgot Password":
        if st.button("Recover Password"):
            if username in users:
                st.info(f"Password: {users[username]}")
            else:
                error_message = "User not found"

    # Custom error (NO RED BOX)
    if error_message:
        st.markdown(f'<div class="error-msg">{error_message}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state["start_app"]:

    st.markdown("<h1 style='color:white;text-align:center;'>Groww Your Wealth 📈</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:white;text-align:center;'>Analyze Stocks & Forecast Trends</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("NIFTY 50", "22,300", "-1.2%")
    col2.metric("BANKNIFTY", "48,200", "-0.8%")
    col3.metric("SENSEX", "73,500", "-1.0%")

    if st.button("🚀 Enter Dashboard"):
        st.session_state["start_app"] = True
        st.rerun()

    st.stop()

# =========================
# 📊 DASHBOARD
# =========================

st.title("📊 Indian Stock Analysis Dashboard")

st.sidebar.header("Settings")

start_date = st.sidebar.date_input("Start Date", d.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", d.date.today())
forecast_days = st.sidebar.slider("Forecast Days", 5, 60, 10)

# Stocks
sector_stocks = {
    "IT": {"TCS":"TCS.NS","Infosys":"INFY.NS","Wipro":"WIPRO.NS"},
    "Banking": {"HDFC":"HDFCBANK.NS","ICICI":"ICICIBANK.NS","SBI":"SBIN.NS"},
    "Energy": {"Reliance":"RELIANCE.NS","ONGC":"ONGC.NS","NTPC":"NTPC.NS"},
    "Auto": {"Maruti":"MARUTI.NS","Tata":"TATAMOTORS.NS","M&M":"M&M.NS"},
    "FMCG": {"ITC":"ITC.NS","HUL":"HINDUNILVR.NS","Dabur":"DABUR.NS"}
}

sector = st.sidebar.selectbox("Sector", list(sector_stocks.keys()))
stock = st.sidebar.selectbox("Stock", list(sector_stocks[sector].keys()))
symbol = sector_stocks[sector][stock]

# ARIMA
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

# Logout
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["start_app"] = False
    st.rerun()

import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="India Finance Analysis", layout="wide")

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state.start_app = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
    url("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f");
    background-size: cover;
}

/* CENTER TITLE (FIXED - NO EXTRA BOX BELOW) */
.center-title {
    text-align:center;
    margin-top:80px;
    color:white;
    font-size:28px;
    font-weight:bold;
}

/* LOGIN BOX */
.login-box {
    background: rgba(255,255,255,0.1);
    padding:30px;
    border-radius:15px;
    backdrop-filter: blur(10px);
    width:350px;
    margin:auto;
    margin-top:40px;
}

/* CLEAN ERROR TEXT */
.error {
    color:#ff6b6b;
    font-size:14px;
    text-align:center;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN SYSTEM
# =========================
if not st.session_state.logged_in:

    # FIXED TITLE (NO EXTRA BOX)
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

    error = ""

    # LOGIN
    if option == "Login":
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                error = "Invalid username or password"

    # SIGN UP
    elif option == "Sign Up":
        if st.button("Create Account"):
            st.success("Account created (Demo Only)")

    # FORGOT PASSWORD
    elif option == "Forgot Password":
        if st.button("Recover Password"):
            if username in users:
                st.info(f"Your password is: {users[username]}")
            else:
                error = "User not found"

    # CLEAN ERROR (NO RED STRIP)
    if error:
        st.markdown(f'<div class="error">{error}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state.start_app:

    st.markdown("<h1 style='color:white;text-align:center;'>📈 Groww Your Wealth</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:white;text-align:center;'>Analyze Stocks & Forecast Trends</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("NIFTY 50", "22,300", "-1.2%")
    col2.metric("BANKNIFTY", "48,200", "-0.8%")
    col3.metric("SENSEX", "73,500", "-1.0%")

    if st.button("🚀 Enter Dashboard"):
        st.session_state.start_app = True
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

# STOCKS
stocks = {
    "TCS":"TCS.NS",
    "Infosys":"INFY.NS",
    "Reliance":"RELIANCE.NS",
    "HDFC Bank":"HDFCBANK.NS"
}

stock = st.sidebar.selectbox("Select Stock", list(stocks.keys()))
symbol = stocks[stock]

# DATA
df = yf.download(symbol, start=start_date, end=end_date)

if not df.empty:
    df = df[['Close']]

    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=forecast_days)
    future_dates = pd.date_range(df.index[-1], periods=forecast_days+1, freq='B')[1:]

    # 📊 FIXED GRAPH (CLEAR DATES)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df.index, df['Close'], label="Actual Price")
    ax.plot(future_dates, forecast, '--', label="Forecast")

    ax.set_title(f"{stock} Price Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    # 👉 DATE FORMAT FIX
    fig.autofmt_xdate()

    ax.legend()

    st.pyplot(fig)

    st.dataframe(pd.DataFrame({"Forecast": forecast.values}, index=future_dates))

# LOGOUT
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.start_app = False
    st.rerun()

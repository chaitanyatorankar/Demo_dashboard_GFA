import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="India Finance Analysis", layout="wide")

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state["start_app"] = False
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "portfolio" not in st.session_state:
    st.session_state["portfolio"] = []
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# --- CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
    url("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f");
    background-size: cover;
}
.title {text-align:center;color:white;font-size:44px;margin-top:40px;font-weight:700;}
.subtitle {text-align:center;color:#aaa;margin-bottom:30px;}
.card {
    background: rgba(255,255,255,0.08);
    padding:25px;border-radius:18px;text-align:center;color:white;
    transition:0.3s;
}
.card:hover {transform: scale(1.05);background: rgba(255,255,255,0.15);}
.login-box {
    background: rgba(255,255,255,0.1);
    padding:35px;border-radius:20px;
    backdrop-filter: blur(15px);
    width:350px;margin:auto;margin-top:40px;
}
.navbar {
    display:flex;
    justify-content:center;
    gap:30px;
    margin-top:20px;
}
.nav-btn {
    padding:10px 20px;
    border-radius:10px;
    background:#ffffff20;
    color:white;
    cursor:pointer;
}
</style>
""", unsafe_allow_html=True)

# ================= NAVBAR =================
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("🏠 Home"):
        st.session_state["page"] = "Home"
with col2:
    if st.button("ℹ️ About"):
        st.session_state["page"] = "About"
with col3:
    if st.button("🔐 Login"):
        st.session_state["page"] = "Login"

# ================= HOME PAGE =================
if st.session_state["page"] == "Home" and not st.session_state["logged_in"]:
    st.markdown('<div class="title">🚀 Stock Sense Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart AI-based Stock Prediction Platform</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card">📊<br><b>Analyze Stocks</b><br>Deep insights of Indian market</div>', unsafe_allow_html=True)
    c2.markdown('<div class="card">🔮<br><b>Forecast Prices</b><br>AI-based predictions</div>', unsafe_allow_html=True)
    c3.markdown('<div class="card">⚡<br><b>Live Data</b><br>Real-time stock tracking</div>', unsafe_allow_html=True)

    st.markdown("### 📌 Why Use This App?")
    st.write("""
    - 📈 Real-time Indian stock market data  
    - 🤖 AI-powered forecasting (ARIMA)  
    - 📊 Sector-wise stock analysis  
    - 💡 Beginner-friendly interface  
    """)

    st.stop()

# ================= ABOUT PAGE =================
if st.session_state["page"] == "About" and not st.session_state["logged_in"]:
    st.markdown('<div class="title">ℹ️ About This Web App</div>', unsafe_allow_html=True)

    st.write("""
    ### 📊 Stock Sense Analytics

    This web application is designed to help users analyze and predict Indian stock market trends.

    ### 🚀 Features:
    - Live Market Data (NIFTY, SENSEX, etc.)
    - Sector-wise Stock Analysis
    - Time Series Forecasting using ARIMA
    - Interactive Dashboard (Streamlit)

    ### 🧠 Technologies Used:
    - Python
    - Streamlit
    - Pandas, NumPy
    - yFinance API
    - Statsmodels (ARIMA)

    ### 👨‍💻 Developed By:
    Chaitanya Torankar

    ### 🎯 Goal:
    To simplify stock analysis and help users make better financial decisions.
    """)

    st.stop()

# ================= LOGIN =================
if not st.session_state["logged_in"]:
    if st.session_state["page"] == "Login":

        st.markdown('<div class="title">🔐 Login to Continue</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        option = st.radio("", ["Login", "Sign Up", "Forgot Password"])
        username = st.text_input("Username")
        password = ""

        if option != "Forgot Password":
            password = st.text_input("Password", type="password")

        users = {"admin": "1234", "chaitanya": "finance123", "demo": "demo123"}

        if option == "Login":
            if st.button("Login"):
                if username in users and users[username] == password:
                    st.session_state["logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid login")

        elif option == "Sign Up":
            if st.button("Create Account"):
                st.success("Account created (Demo)")

        elif option == "Forgot Password":
            if st.button("Recover"):
                if username in users:
                    st.info(f"Password: {users[username]}")
                else:
                    st.error("User not found")

        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

# ================= YOUR ORIGINAL APP CONTINUES =================
# (NO CHANGE BELOW)

# ================= HOMEPAGE =================
if not st.session_state["start_app"]:

    st.markdown('<div class="title">📈 Indian Stock Analysis Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict • Analyze • Grow your Wealth</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card">📊<br><b>Stock Analysis</b></div>', unsafe_allow_html=True)
    c2.markdown('<div class="card">🔮<br><b>Forecasting</b></div>', unsafe_allow_html=True)
    c3.markdown('<div class="card">⚡<br><b>Live Data</b></div>', unsafe_allow_html=True)

    if st.button("🚀 Start Analysis Now"):
        st.session_state["start_app"] = True
        st.rerun()

    st.stop()

# ================= DASHBOARD =================
st.title("📊 Stock Dashboard")

st.sidebar.header("Settings")

start_date = st.sidebar.date_input("Start Date", d.date(2022,1,1))
end_date = st.sidebar.date_input("End Date", d.date.today())

forecast_days = st.sidebar.slider("Forecast Days", 5, 90, 30)

sector_stocks = {
    "IT": {"TCS":"TCS.NS","Infosys":"INFY.NS"},
    "Banking": {"HDFC Bank":"HDFCBANK.NS","ICICI":"ICICIBANK.NS"},
    "FMCG": {"ITC":"ITC.NS","HUL":"HINDUNILVR.NS"}
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

# LOGOUT
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["start_app"] = False
    st.session_state["page"] = "Home"
    st.rerun()

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
    st.session_state["start_app"] = False
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- CSS (NEW MODERN UI LIKE IMAGE) ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)),
    url("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f");
    background-size: cover;
}

.title {
    text-align:center;
    color:white;
    font-size:42px;
    font-weight:bold;
    margin-top:50px;
}

.subtitle {
    text-align:center;
    color:#ccc;
    margin-bottom:40px;
}

.card {
    background: rgba(255,255,255,0.08);
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
}

.login-box {
    background: rgba(255,255,255,0.1);
    padding:30px;
    border-radius:15px;
    backdrop-filter: blur(10px);
    width:350px;
    margin:auto;
    margin-top:40px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN SYSTEM
# =========================
if not st.session_state["logged_in"]:

    st.markdown('<div class="title">🇮🇳 Indian Stock Analysis Platform</div>', unsafe_allow_html=True)

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

    if option == "Login":
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid username or password")

    elif option == "Sign Up":
        if st.button("Create Account"):
            st.success("Account created (Demo Only)")

    elif option == "Forgot Password":
        if st.button("Recover Password"):
            if username in users:
                st.info(f"Password: {users[username]}")
            else:
                st.error("User not found")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 HOMEPAGE (NEW DESIGN)
# =========================
if not st.session_state["start_app"]:

    st.markdown('<div class="title">🚀 Indian Stock Analysis Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict • Analyze • Grow your Wealth</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.markdown('<div class="card">📊<br><b>Stock Analysis</b><br>Analyze historical data</div>', unsafe_allow_html=True)
    col2.markdown('<div class="card">🔮<br><b>Forecasting</b><br>Predict future prices</div>', unsafe_allow_html=True)
    col3.markdown('<div class="card">⚡<br><b>Live Data</b><br>Real-time updates</div>', unsafe_allow_html=True)

    st.markdown("### 📊 Market Overview")

    m1, m2, m3 = st.columns(3)
    m1.metric("NIFTY 50", "22,300", "-1.2%")
    m2.metric("BANKNIFTY", "48,200", "-0.8%")
    m3.metric("SENSEX", "73,500", "-1.0%")

    if st.button("🚀 Start Analysis Now"):
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

# ✅ UPDATED FORECAST LIMIT (2–3 MONTHS)
forecast_days = st.sidebar.slider("Forecast Days", 5, 90, 30)

# STOCKS
sector_stocks = {
    "IT": {
        "TCS":"TCS.NS",
        "Infosys":"INFY.NS",
        "Wipro":"WIPRO.NS",
        "HCL Tech":"HCLTECH.NS",
        "Tech Mahindra":"TECHM.NS"
    },
    "Banking": {
        "HDFC Bank":"HDFCBANK.NS",
        "ICICI Bank":"ICICIBANK.NS",
        "SBI":"SBIN.NS",
        "Axis Bank":"AXISBANK.NS",
        "Kotak Bank":"KOTAKBANK.NS"
    },
    "FMCG": {
        "ITC":"ITC.NS",
        "HUL":"HINDUNILVR.NS",
        "Nestle":"NESTLEIND.NS",
        "Britannia":"BRITANNIA.NS",
        "Dabur":"DABUR.NS"
    },
    "Energy": {
        "Reliance":"RELIANCE.NS",
        "ONGC":"ONGC.NS",
        "NTPC":"NTPC.NS",
        "Power Grid":"POWERGRID.NS",
        "Coal India":"COALINDIA.NS"
    },
    "Auto": {
        "Maruti":"MARUTI.NS",
        "Tata Motors":"TATAMOTORS.NS",
        "M&M":"M&M.NS",
        "Bajaj Auto":"BAJAJ-AUTO.NS",
        "Hero MotoCorp":"HEROMOTOCO.NS"
    }
}

sector = st.sidebar.selectbox("Sector", list(sector_stocks.keys()))
stock = st.sidebar.selectbox("Stock", list(sector_stocks[sector].keys()))
symbol = sector_stocks[sector][stock]

# DATA
df = yf.download(symbol, start=start_date, end=end_date)

if not df.empty:
    df = df[['Close']]

    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=forecast_days)

    future_dates = pd.date_range(df.index[-1], periods=forecast_days+1, freq='B')[1:]

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df.index, df['Close'], label="Actual Price")
    ax.plot(future_dates, forecast, '--', label="Forecast")

    ax.set_title(f"{stock} Price Forecast")
    ax.legend()

    st.pyplot(fig)

    st.dataframe(pd.DataFrame({"Forecast": forecast.values}, index=future_dates))

# LOGOUT
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["start_app"] = False
    st.rerun()

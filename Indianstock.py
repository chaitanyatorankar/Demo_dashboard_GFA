import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Indian Stock Analysis", layout="wide")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "start_app" not in st.session_state:
    st.session_state.start_app = False

# --- CSS (FULL CENTER + ANIMATION) ---
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
    url("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f");
    background-size: cover;
    background-position: center;
}

/* Center Wrapper (FULL CENTER) */
.center-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 90vh;
}

/* Glass Login Box */
.login-box {
    background: rgba(255,255,255,0.1);
    padding: 40px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    width: 380px;
    text-align: center;
    animation: fadeSlide 1.2s ease;
}

/* Title */
.title {
    color: white;
    font-size: 26px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Animation */
@keyframes fadeSlide {
    from {
        opacity: 0;
        transform: translateY(40px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Error */
.error {
    color: #ff4b4b;
    font-size: 14px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN PAGE
# =========================
if not st.session_state.logged_in:

    st.markdown('<div class="center-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    st.markdown('<div class="title">🇮🇳 Welcome to Indian Stock Analysis</div>', unsafe_allow_html=True)

    option = st.radio("", ["Login", "Sign Up", "Forgot Password"])

    username = st.text_input("Username")
    password = ""

    if option != "Forgot Password":
        password = st.text_input("Password", type="password")

    users = {
        "admin": "1234",
        "chaitanya": "finance123"
    }

    error = ""

    if option == "Login":
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                error = "Invalid username or password"

    elif option == "Sign Up":
        if st.button("Create Account"):
            st.success("Account created (Demo)")

    elif option == "Forgot Password":
        if st.button("Recover Password"):
            if username in users:
                st.info(f"Password: {users[username]}")
            else:
                error = "User not found"

    if error:
        st.markdown(f'<div class="error">{error}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state.start_app:

    st.markdown("<h1 style='color:white;text-align:center;'>📈 Groww Your Wealth</h1>", unsafe_allow_html=True)

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

start_date = st.sidebar.date_input("Start Date", d.date(2022,1,1))
end_date = st.sidebar.date_input("End Date", d.date.today())
forecast_days = st.sidebar.slider("Forecast Days", 5, 60, 10)

stocks = {
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "Reliance": "RELIANCE.NS",
    "HDFC Bank": "HDFCBANK.NS"
}

stock = st.sidebar.selectbox("Select Stock", list(stocks.keys()))
symbol = stocks[stock]

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
    st.session_state.logged_in = False
    st.session_state.start_app = False
    st.rerun()

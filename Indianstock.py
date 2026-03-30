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

/* Center Title */
.center-title {
    text-align:center;
    margin-top:60px;
    background: rgba(255,255,255,0.1);
    padding:15px;
    border-radius:15px;
    backdrop-filter: blur(10px);
    color:white;
    font-size:26px;
    font-weight:bold;
    width:450px;
    margin-left:auto;
    margin-right:auto;
}

/* Login Box */
.login-box {
    background: rgba(255,255,255,0.1);
    padding:30px;
    border-radius:15px;
    backdrop-filter: blur(10px);
    width:400px;
    margin:auto;
    text-align:center;
}

/* Homepage Cards */
.card {
    background: rgba(255,255,255,0.1);
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    transition:0.3s;
}
.card:hover {
    transform: scale(1.05);
}

/* Error */
.error {
    color:#ff4b4b;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN
# =========================
if not st.session_state.logged_in:

    st.markdown('<div class="center-title">🇮🇳 Welcome to Indian Stock Analysis</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    option = st.radio("", ["Login", "Sign Up", "Forgot Password"])

    username = st.text_input("Username")
    password = ""

    if option != "Forgot Password":
        password = st.text_input("Password", type="password")

    users = {"admin":"1234","chaitanya":"finance123"}

    error=""

    if option=="Login":
        if st.button("Login"):
            if username in users and users[username]==password:
                st.session_state.logged_in=True
                st.rerun()
            else:
                error="Invalid username or password"

    elif option=="Sign Up":
        if st.button("Create Account"):
            st.success("Account created (Demo)")

    elif option=="Forgot Password":
        if st.button("Recover"):
            if username in users:
                st.info(f"Password: {users[username]}")
            else:
                error="User not found"

    if error:
        st.markdown(f'<div class="error">{error}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 PREMIUM HOMEPAGE
# =========================
if not st.session_state.start_app:

    # HERO
    st.markdown("""
    <h1 style='text-align:center;color:white;font-size:50px;'>
    🚀 Indian Stock Analysis Platform
    </h1>
    <p style='text-align:center;color:lightgray;font-size:18px;'>
    Predict • Analyze • Grow your Wealth 📊
    </p>
    """, unsafe_allow_html=True)

    st.write("")

    # CARDS
    col1,col2,col3 = st.columns(3)

    col1.markdown("""
    <div class="card">
    <h3>📊 Stock Analysis</h3>
    <p>Analyze historical data</p>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown("""
    <div class="card">
    <h3>🔮 Forecasting</h3>
    <p>Predict future prices</p>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown("""
    <div class="card">
    <h3>⚡ Live Data</h3>
    <p>Real-time updates</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # MARKET
    st.subheader("📊 Market Overview")

    col1,col2,col3 = st.columns(3)
    col1.metric("NIFTY 50","22,300","-1.2%")
    col2.metric("BANKNIFTY","48,200","-0.8%")
    col3.metric("SENSEX","73,500","-1.0%")

    st.write("")

    if st.button("🚀 Start Analysis Now"):
        st.session_state.start_app=True
        st.rerun()

    st.stop()

# =========================
# 📊 DASHBOARD
# =========================

st.title("📊 Indian Stock Analysis Dashboard")

st.sidebar.header("Settings")

start_date = st.sidebar.date_input("Start Date", d.date(2022,1,1))
end_date = st.sidebar.date_input("End Date", d.date.today())
forecast_days = st.sidebar.slider("Forecast Days",5,60,10)

stocks={
    "TCS":"TCS.NS",
    "Infosys":"INFY.NS",
    "Reliance":"RELIANCE.NS",
    "HDFC Bank":"HDFCBANK.NS"
}

stock=st.sidebar.selectbox("Select Stock",list(stocks.keys()))
symbol=stocks[stock]

df=yf.download(symbol,start=start_date,end=end_date)

if not df.empty:
    df=df[['Close']]

    model=ARIMA(df['Close'],order=(5,1,0))
    model_fit=model.fit()

    forecast=model_fit.forecast(steps=forecast_days)
    future_dates=pd.date_range(df.index[-1],periods=forecast_days+1,freq='B')[1:]

    fig,ax=plt.subplots()
    ax.plot(df.index,df['Close'],label="Actual")
    ax.plot(future_dates,forecast,'--',label="Forecast")
    ax.legend()

    st.pyplot(fig)
    st.dataframe(pd.DataFrame({"Forecast":forecast.values},index=future_dates))

# Logout
if st.sidebar.button("Logout"):
    st.session_state.logged_in=False
    st.session_state.start_app=False
    st.rerun()

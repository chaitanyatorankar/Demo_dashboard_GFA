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
.signal-buy {padding:15px;background:#0f5132;border-radius:10px;color:white;}
.signal-sell {padding:15px;background:#842029;border-radius:10px;color:white;}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if not st.session_state["logged_in"]:
    st.markdown('<div class="title">🚀 Stock Sense Analytics</div>', unsafe_allow_html=True)
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

# ================= HOMEPAGE =================
if not st.session_state["start_app"]:

    st.markdown('<div class="title">📈 Indian Stock Analysis Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict • Analyze • Grow your Wealth</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card">📊<br><b>Stock Analysis</b></div>', unsafe_allow_html=True)
    c2.markdown('<div class="card">🔮<br><b>Forecasting</b></div>', unsafe_allow_html=True)
    c3.markdown('<div class="card">⚡<br><b>Live Data</b></div>', unsafe_allow_html=True)

    # ===== LIVE MARKET =====
    st.markdown("## 📊 Market Overview (Live)")

    indices = {
        "NIFTY 50": "^NSEI",
        "BANKNIFTY": "^NSEBANK",
        "SENSEX": "^BSESN",
        "NIFTY IT": "^CNXIT",
        "NIFTY FMCG": "^CNXFMCG",
        "NIFTY AUTO": "^CNXAUTO"
    }

    idx_list = list(indices.items())

    for i in range(0, len(idx_list), 3):
        row = idx_list[i:i+3]
        cols = st.columns(3)

        for j, (name, symbol) in enumerate(row):
            try:
                data = yf.download(symbol, period="2d", progress=False)
                latest = float(data["Close"].iloc[-1])
                prev = float(data["Close"].iloc[-2])
                pct = ((latest - prev) / prev) * 100
                cols[j].metric(name, f"{latest:,.0f}", f"{pct:.2f}%")
            except:
                cols[j].metric(name, "N/A", "0%")

    # ===== TOP STOCKS =====
    st.markdown("### 🔥 Top Stocks Live")

    stocks = {
        "Reliance": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Infosys": "INFY.NS",
        "ITC": "ITC.NS",
        "Tata Motors": "TATAMOTORS.NS"
    }

    st_list = list(stocks.items())

    for i in range(0, len(st_list), 3):
        row = st_list[i:i+3]
        cols = st.columns(3)

        for j, (name, sym) in enumerate(row):
            try:
                data = yf.download(sym, period="2d", progress=False)
                latest = float(data["Close"].iloc[-1])
                prev = float(data["Close"].iloc[-2])
                pct = ((latest - prev) / prev) * 100
                cols[j].metric(name, f"₹{latest:.2f}", f"{pct:.2f}%")
            except:
                cols[j].metric(name, "N/A", "0%")

    if st.button("🚀 Start Analysis Now"):
        st.session_state["start_app"] = True
        st.rerun()

    st.stop()

# ================= DASHBOARD =================
st.title("📊 Stock Dashboard")

start_date = st.sidebar.date_input("Start Date", d.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", d.date.today())
forecast_days = st.sidebar.slider("Forecast Days", 5, 90, 30)

symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., TCS.NS)", "TCS.NS")

df = yf.download(symbol, start=start_date, end=end_date, progress=False)

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

    # SAFE SIGNAL
    predicted_price = float(np.array(forecast)[-1])
    last_price = float(df['Close'].iloc[-1])

    st.subheader("📢 AI Signal")

    if predicted_price > last_price:
        st.markdown(f"<div class='signal-buy'>🟢 BUY</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='signal-sell'>🔴 SELL</div>", unsafe_allow_html=True)

# ================= PORTFOLIO =================
st.subheader("💼 Portfolio")

p_stock = st.text_input("Stock Symbol")
p_qty = st.number_input("Qty", 1)
p_price = st.number_input("Buy Price", 1.0)

if st.button("Add"):
    st.session_state["portfolio"].append({
        "Stock": p_stock,
        "Qty": p_qty,
        "Buy Price": p_price
    })

if st.session_state["portfolio"]:
    pf = pd.DataFrame(st.session_state["portfolio"])
    st.dataframe(pf)

# ================= LOGOUT =================
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["start_app"] = False
    st.rerun()

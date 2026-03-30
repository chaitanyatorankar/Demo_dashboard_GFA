import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as d
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh   # ✅ FIX

# --- Page Config ---
st.set_page_config(page_title="FinForecast Pro", layout="wide")

# --- Auto Refresh ---
st_autorefresh(interval=60000, key="refresh")

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state["start_app"] = False

# --- CSS ---
st.markdown("""
<style>
.main-title {
    font-size: 52px;
    font-weight: 800;
    text-align: center;
}
.sub-text {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state["start_app"]:

    st.markdown('<div class="main-title">FinForecast Pro 🔮</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">AI Stock Forecasting App</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("NIFTY 50", "22,300", "-1.2%")
    col2.metric("BANKNIFTY", "48,200", "-0.8%")
    col3.metric("SENSEX", "73,500", "-1.0%")

    if st.button("🚀 Get Started"):
        st.session_state["start_app"] = True
        st.rerun()

    st.stop()

# =========================
# 📊 DASHBOARD
# =========================
st.title("📊 FinForecast Pro Dashboard")

st.sidebar.header("⚙️ Settings")

start_date = st.sidebar.date_input("Start Date", d.date(2022,1,1))
end_date = st.sidebar.date_input("End Date", d.date.today())

forecast_days = st.sidebar.number_input("Forecast Days", 5, 60, 10)

sector_stocks = {
    "IT": {"TCS": "TCS.NS", "Infosys": "INFY.NS"},
    "Banking": {"HDFC": "HDFCBANK.NS", "ICICI": "ICICIBANK.NS"}
}

sector = st.sidebar.selectbox("Sector", list(sector_stocks.keys()))
stock = st.sidebar.selectbox("Stock", list(sector_stocks[sector].keys()))
symbol = sector_stocks[sector][stock]

# =========================
# 📡 LIVE DATA
# =========================
live = yf.download(symbol, period="1d", interval="1m")

if not live.empty:
    st.metric("Live Price", f"₹{live['Close'].iloc[-1]:.2f}")

# =========================
# 📊 ARIMA
# =========================
def arima_model(symbol):
    df = yf.download(symbol, start=start_date, end=end_date)
    df = df[['Close']].dropna().reset_index()

    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=forecast_days)

    future_dates = pd.date_range(df['Date'].iloc[-1], periods=forecast_days+1, freq='B')[1:]

    forecast_df = pd.DataFrame({"Date": future_dates, "Forecast": forecast})

    return df, forecast_df

df, forecast_df = arima_model(symbol)

# =========================
# 📈 PLOT
# =========================
fig = go.Figure()

fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name="Actual"))
fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Forecast'],
                         name="Forecast", line=dict(dash='dash')))

st.plotly_chart(fig, use_container_width=True)

# =========================
# 🧠 INSIGHT
# =========================
if forecast_df['Forecast'].iloc[-1] > df['Close'].iloc[-1]:
    st.success("📈 Uptrend Expected")
else:
    st.error("📉 Downtrend Expected")

# =========================
# 📊 TABLE
# =========================
st.dataframe(forecast_df)

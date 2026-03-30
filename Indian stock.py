import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as d
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="FinForecast Pro", layout="wide")

# --- Auto Refresh (Real-time feel) ---
st.autorefresh(interval=60000, key="refresh")

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state["start_app"] = False

# --- Custom CSS ---
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #eef2f3, #dfe9f3);
}

.main-title {
    font-size: 52px;
    font-weight: 800;
    text-align: center;
    color: #1f3b73;
}

.sub-text {
    font-size: 22px;
    text-align: center;
    color: #555;
}

.stButton>button {
    background-color: #00b386;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    padding: 10px 24px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state["start_app"]:

    st.markdown('<div class="main-title">FinForecast Pro 🔮</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Smart Stock Analysis & AI Forecasting for Indian Markets</div>', unsafe_allow_html=True)

    st.write("")

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("NIFTY 50", "22,300", "-1.2%")
    col2.metric("BANKNIFTY", "48,200", "-0.8%")
    col3.metric("SENSEX", "73,500", "-1.0%")

    st.write("")

    if st.button("🚀 Get Started"):
        st.session_state["start_app"] = True
        st.rerun()

    st.stop()

# =========================
# 📊 MAIN DASHBOARD
# =========================

st.title("🇮🇳 FinForecast Pro - Stock Analysis Dashboard")

# --- Sidebar ---
st.sidebar.header("⚙️ Customize Analysis")

default_start = d.date(2022, 1, 1)
default_end = d.date(2025, 7, 10)

start_date = st.sidebar.date_input("📅 Start Date", default_start,
                                   min_value=d.date(2015, 1, 1),
                                   max_value=d.date.today())

end_date = st.sidebar.date_input("📅 End Date", default_end,
                                 min_value=start_date,
                                 max_value=d.date.today())

forecast_days = st.sidebar.number_input(
    "🔮 Forecast Days",
    min_value=5, max_value=60, value=10, step=5
)

# --- Stock Data ---
sector_stocks = {
    "IT": {
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "Wipro": "WIPRO.NS"
    },
    "Banking": {
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS"
    }
}

sector_choice = st.sidebar.selectbox("🏢 Sector", list(sector_stocks.keys()))
stock_choice = st.sidebar.selectbox("📌 Stock", list(sector_stocks[sector_choice].keys()))
symbol = sector_stocks[sector_choice][stock_choice]

# =========================
# 📡 LIVE DATA
# =========================
live_data = yf.download(symbol, period="1d", interval="1m")

if not live_data.empty:
    latest_price = live_data['Close'].iloc[-1]
    prev_price = live_data['Close'].iloc[0]
    change = latest_price - prev_price

    st.metric(f"📡 Live Price - {stock_choice}", f"₹{latest_price:.2f}", f"{change:.2f}")

# =========================
# 📊 ARIMA FUNCTIONS
# =========================
def check_stationarity(timeseries):
    result = adfuller(timeseries.dropna())
    return result[1] <= 0.05

def arima_analysis(symbol, start, end, steps):
    df = yf.download(symbol, start=start, end=end)
    df = df[['Close']].dropna().reset_index()

    df['Diff'] = df['Close'].diff()

    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=steps)

    future_dates = pd.date_range(df['Date'].iloc[-1], periods=steps+1, freq='B')[1:]

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Forecast": forecast.values
    })

    return df, forecast_df

# =========================
# 🚀 RUN ANALYSIS
# =========================
df, forecast_df = arima_analysis(symbol, start_date, end_date, forecast_days)

# =========================
# 📈 PLOT (INTERACTIVE)
# =========================
st.subheader("📈 Stock Forecast")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Close'],
    mode='lines', name='Actual'
))

fig.add_trace(go.Scatter(
    x=forecast_df['Date'], y=forecast_df['Forecast'],
    mode='lines', name='Forecast',
    line=dict(dash='dash')
))

st.plotly_chart(fig, use_container_width=True)

# =========================
# 🧠 AI INSIGHT
# =========================
if forecast_df['Forecast'].iloc[-1] > df['Close'].iloc[-1]:
    st.success("📈 AI Insight: Uptrend Expected")
else:
    st.error("📉 AI Insight: Downtrend Expected")

# =========================
# 📊 DATA TABLE
# =========================
st.subheader("🔢 Forecast Data")
st.dataframe(forecast_df.set_index("Date"))

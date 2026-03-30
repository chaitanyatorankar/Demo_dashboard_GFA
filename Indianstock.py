import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# --- Config ---
st.set_page_config(page_title="FinForecast Pro", layout="wide")

# --- Auto Refresh ---
st_autorefresh(interval=60000, key="refresh")

# --- Session ---
if "start_app" not in st.session_state:
    st.session_state["start_app"] = False

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state["start_app"]:

    st.title("🔮 FinForecast Pro")
    st.write("AI Stock Forecasting Web App")

    col1, col2, col3 = st.columns(3)
    col1.metric("NIFTY 50", "22,300")
    col2.metric("BANKNIFTY", "48,200")
    col3.metric("SENSEX", "73,500")

    if st.button("🚀 Start"):
        st.session_state["start_app"] = True
        st.rerun()

    st.stop()

# =========================
# 📊 DASHBOARD
# =========================
st.title("📊 Stock Dashboard")

# Sidebar
start_date = st.sidebar.date_input("Start Date", d.date(2022,1,1))
end_date = st.sidebar.date_input("End Date", d.date.today())
forecast_days = st.sidebar.number_input("Forecast Days", 5, 60, 10)

stocks = {
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC": "HDFCBANK.NS"
}

stock = st.sidebar.selectbox("Stock", list(stocks.keys()))
symbol = stocks[stock]

# =========================
# 📡 LIVE PRICE FIX
# =========================
live = yf.download(symbol, period="1d", interval="1m")

if not live.empty:
    try:
        latest_price = float(live['Close'].iloc[-1])
        st.metric("📡 Live Price", f"₹{latest_price:.2f}")
    except:
        st.warning("Live data not available")

# =========================
# 📊 ARIMA
# =========================
def model(symbol):
    df = yf.download(symbol, start=start_date, end=end_date)
    df = df[['Close']].dropna().reset_index()

    model = ARIMA(df['Close'], order=(5,1,0))
    fit = model.fit()

    forecast = fit.forecast(steps=forecast_days)

    future = pd.date_range(df['Date'].iloc[-1], periods=forecast_days+1, freq='B')[1:]

    forecast_df = pd.DataFrame({"Date": future, "Forecast": forecast})

    return df, forecast_df

df, forecast_df = model(symbol)

# =========================
# 📈 GRAPH
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

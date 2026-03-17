import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as d
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="India Finance Analysis - ARIMA Forecast", layout="wide")
st.sidebar.header("⚙️ Customize Analysis")

# --- Date Inputs ---
default_start = d.date(2022, 1, 1)
default_end = d.date(2025, 7, 10)

start_date = st.sidebar.date_input("📅 Start Date", default_start,
                                   min_value=d.date(2015, 1, 1),
                                   max_value=d.date.today())

end_date = st.sidebar.date_input("📅 End Date", default_end,
                                 min_value=start_date,
                                 max_value=d.date.today())

# --- Forecast Days ---
forecast_days = st.sidebar.number_input(
    "🔮 Forecast Days (Business Days)",
    min_value=5, max_value=60, value=10, step=5
)

# --- Stationarity Function ---
def check_stationarity(timeseries):
    result = adfuller(timeseries.dropna())
    return {
        'ADF Statistic': result[0],
        'p-value': result[1],
        'Stationary': result[1] <= 0.05
    }

# --- ARIMA Function ---
def arima_analysis(stock_symbol, label, s, e, forecast_horizon):
    df = yf.download(stock_symbol, start=s, end=e, auto_adjust=False)

    if df.empty:
        st.error(f"No data found for {label}")
        return None, None

    df = df[['Close']].copy().reset_index()
    df.dropna(inplace=True)

    # Stationarity
    stat_close = check_stationarity(df['Close'])
    df['Close_Diff'] = df['Close'].diff()
    stat_diff = check_stationarity(df['Close_Diff'])

    # ARIMA Model
    model = ARIMA(df['Close'], order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast
    forecast = model_fit.forecast(steps=forecast_horizon)
    future_dates = pd.date_range(
        start=df['Date'].iloc[-1],
        periods=forecast_horizon + 1,
        freq='B'
    )[1:]

    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Forecast': forecast.values
    })

    return forecast_df, (stat_close, stat_diff, df)

# --- India Stocks Only ---
sector_stocks = {
    "IT": {
        "TCS": "TCS.NS",
        "Wipro": "WIPRO.NS",
        "Infosys": "INFY.NS",
        "HCL Technologies": "HCLTECH.NS",
        "Tech Mahindra": "TECHM.NS"
    },
    "Banking": {
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS"
    }
}

# --- UI ---
st.title("🇮🇳 India Finance Analysis with ARIMA Forecast")
st.markdown("Analyze Indian IT & Banking stocks and forecast trends using ARIMA.")

# --- Selection ---
sector_choice = st.sidebar.selectbox("🏢 Select Sector", list(sector_stocks.keys()))
stock_choice = st.sidebar.selectbox("📌 Select Stock", list(sector_stocks[sector_choice].keys()))
symbol = sector_stocks[sector_choice][stock_choice]

# --- Run Analysis ---
forecast_df, results = arima_analysis(symbol, stock_choice, start_date, end_date, forecast_days)

if forecast_df is not None:
    stat_close, stat_diff, df = results

    # --- Stationarity Results ---
    st.subheader(f"📊 Stationarity Check - {stock_choice}")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Original Series**")
        st.write(f"ADF Statistic: {stat_close['ADF Statistic']:.4f}")
        st.write(f"p-value: {stat_close['p-value']:.4f}")
        st.write("✅ Stationary" if stat_close['Stationary'] else "❌ Not Stationary")

    with col2:
        st.write("**Differenced Series**")
        st.write(f"ADF Statistic: {stat_diff['ADF Statistic']:.4f}")
        st.write(f"p-value: {stat_diff['p-value']:.4f}")
        st.write("✅ Stationary" if stat_diff['Stationary'] else "❌ Not Stationary")

    # --- Plot ---
    st.subheader("📈 Forecast Plot")
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df['Date'], df['Close'], label='Actual Price')
    ax.plot(forecast_df['Date'], forecast_df['Forecast'],
            linestyle='--', label=f'{forecast_days}-Day Forecast')

    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title(f"{stock_choice} Price Forecast")
    ax.legend()

    st.pyplot(fig)

    # --- Forecast Table ---
    st.subheader("🔢 Forecast Values")
    st.dataframe(forecast_df.set_index('Date'))

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

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state["start_app"] = False

# --- Custom CSS ---
st.markdown("""
    <style>
    .main-title {
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        color: #2e3a59;
    }
    .sub-text {
        font-size: 20px;
        text-align: center;
        color: #6c757d;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state["start_app"]:

    st.markdown('<div class="main-title">Groww Your Wealth 📈</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Analyze Indian Stocks & Forecast Trends using ARIMA Model</div>', unsafe_allow_html=True)

    st.write("")

    # Optional Image (replace with your file path)
    # st.image("groww_style_image.png", use_container_width=True)

    # Metrics Row (like Groww)
    col1, col2, col3 = st.columns(3)
    col1.metric("NIFTY 50", "22,300", "-1.2%")
    col2.metric("BANKNIFTY", "48,200", "-0.8%")
    col3.metric("SENSEX", "73,500", "-1.0%")

    st.write("")

    # Button
    if st.button("🚀 Get Started"):
        st.session_state["start_app"] = True
        st.rerun()

    st.stop()

# =========================
# 📊 MAIN DASHBOARD
# =========================

st.title("🇮🇳 India Finance Analysis with ARIMA Forecast")
st.markdown("Analyze Indian stocks and forecast trends using ARIMA.")

# --- Sidebar ---
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

# --- India Stocks ---
sector_stocks = {
    "IT": {
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "Wipro": "WIPRO.NS",
        "HCL Technologies": "HCLTECH.NS",
        "Tech Mahindra": "TECHM.NS",
        "LTIMindtree": "LTIM.NS",
        "Mphasis": "MPHASIS.NS"
    },

    "Banking": {
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "State Bank of India": "SBIN.NS",
        "Axis Bank": "AXISBANK.NS",
        "Kotak Mahindra Bank": "KOTAKBANK.NS",
        "IndusInd Bank": "INDUSINDBK.NS"
    },

    "FMCG": {
        "Hindustan Unilever": "HINDUNILVR.NS",
        "ITC": "ITC.NS",
        "Nestle India": "NESTLEIND.NS",
        "Britannia": "BRITANNIA.NS",
        "Dabur": "DABUR.NS"
    },

    "Energy": {
        "Reliance Industries": "RELIANCE.NS",
        "ONGC": "ONGC.NS",
        "NTPC": "NTPC.NS",
        "Power Grid": "POWERGRID.NS",
        "Coal India": "COALINDIA.NS"
    },

    "Automobile": {
        "Maruti Suzuki": "MARUTI.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "Mahindra & Mahindra": "M&M.NS",
        "Bajaj Auto": "BAJAJ-AUTO.NS",
        "Hero MotoCorp": "HEROMOTOCO.NS"
    }
}

# --- Selection ---
sector_choice = st.sidebar.selectbox("🏢 Select Sector", list(sector_stocks.keys()))
stock_choice = st.sidebar.selectbox("📌 Select Stock", list(sector_stocks[sector_choice].keys()))
symbol = sector_stocks[sector_choice][stock_choice]

# --- Run Analysis ---
forecast_df, results = arima_analysis(symbol, stock_choice, start_date, end_date, forecast_days)

if forecast_df is not None:
    stat_close, stat_diff, df = results

    # --- Stationarity ---
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

    # --- Table ---
    st.subheader("🔢 Forecast Values")
    st.dataframe(forecast_df.set_index('Date'))

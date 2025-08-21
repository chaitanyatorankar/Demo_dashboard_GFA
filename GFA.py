import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# ----------------------------
# Sidebar - User Inputs
# ----------------------------
st.sidebar.title("⚙️ Controls")

# Stock Selector
stocks = {
    "Infosys (INFY)": "INFY.NS",
    "TCS (TCS)": "TCS.NS",
    "Nifty 50": "^NSEI",
    "NASDAQ": "^IXIC",
    "London FTSE": "^FTSE",
    "Tokyo Nikkei": "^N225",
    "Shanghai Composite": "000001.SS"
}
stock_choice = st.sidebar.selectbox("Select Stock / Index", list(stocks.keys()))

# Date Range
start_date = st.sidebar.date_input("Start Date", dt.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", dt.date.today())

# Forecast Horizon
forecast_days = st.sidebar.slider("Forecast Days", 7, 60, 30)

# ----------------------------
# Fetch Data
# ----------------------------
symbol = stocks[stock_choice]
df = yf.download(symbol, start=start_date, end=end_date)

st.title("📊 Global Finance Analysis & Forecasting with ARIMA")
st.subheader(f"Stock: {stock_choice} ({symbol})")

st.write("### Sample Data")
st.dataframe(df.tail())

# ----------------------------
# Historical Price Chart
# ----------------------------
st.write("### 📈 Historical Closing Prices")
fig, ax = plt.subplots()
ax.plot(df.index, df['Close'], label="Close Price")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
st.pyplot(fig)

# ----------------------------
# ARIMA Forecast
# ----------------------------
st.write("### 🔮 ARIMA Forecast")

# Fit ARIMA model
data = df['Close'].dropna()
model = ARIMA(data, order=(5,1,0))  # Simple ARIMA(5,1,0)
model_fit = model.fit()

# Forecast
forecast = model_fit.forecast(steps=forecast_days)
forecast_index = pd.date_range(data.index[-1], periods=forecast_days+1, freq="D")[1:]
forecast_series = pd.Series(forecast, index=forecast_index)

# Plot Forecast vs Actual
fig2, ax2 = plt.subplots()
ax2.plot(data.index, data, label="Historical")
ax2.plot(forecast_series.index, forecast_series, color="red", label="Forecast")
ax2.set_xlabel("Date")
ax2.set_ylabel("Price")
ax2.legend()
st.pyplot(fig2)

# ----------------------------
# Download Option
# ----------------------------
csv = forecast_series.to_frame(name="Forecasted Price").to_csv().encode("utf-8")
st.download_button(
    label="📥 Download Forecast Data as CSV",
    data=csv,
    file_name=f"{symbol}_forecast.csv",
    mime="text/csv"
)

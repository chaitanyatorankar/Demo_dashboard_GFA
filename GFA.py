import streamlit as st
import pandas as pd
import numpy as np

st.title("Stock Price Dashboard")

# Generate dummy stock data
dates = pd.date_range("2023-01-01", periods=100)
data = pd.DataFrame({
    "Date": dates,
    "Stock Price": np.cumsum(np.random.randn(100)) + 100
})

st.line_chart(data.set_index("Date"))

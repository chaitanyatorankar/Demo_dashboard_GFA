import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="Indian Stock Analysis", layout="wide")

# --- Custom CSS (Image Jaisa Look) ---
st.markdown("""
<style>
    /* Background Image */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)),
        url("https://images.unsplash.com/photo-1611974717482-4800b3f23df5?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Main Title Section */
    .hero-section {
        text-align: center;
        padding: 50px 0;
        color: white;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
        transition: 0.3s;
    }

    /* Metric Styling */
    .metric-val { font-size: 24px; font-weight: bold; margin: 5px 0; }
    .metric-down { color: #ff4b4b; font-size: 14px; }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #2ecc71, #27ae60) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 10px 40px !important;
        font-weight: bold !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state["start_app"] = False

# =========================
# 🏠 HOME PAGE (Reference Image Jaisa)
# =========================
if not st.session_state["start_app"]:
    # Title & Subtitle
    st.markdown("""
    <div class="hero-section">
        <h1>🚀 Indian Stock Analysis Platform</h1>
        <p>Predict • Analyze • Grow your Wealth 📊</p>
    </div>
    """, unsafe_allow_html=True)

    # Top Feature Row
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown('<div class="glass-card">📊<br><b>Stock Analysis</b><p style="font-size:12px">Analyze historical data</p></div>', unsafe_allow_html=True)
    with col_f2:
        st.markdown('<div class="glass-card">🔮<br><b>Forecasting</b><p style="font-size:12px">Predict future prices</p></div>', unsafe_allow_html=True)
    with col_f3:
        st.markdown('<div class="glass-card">⚡<br><b>Live Data</b><p style="font-size:12px">Real-time updates</p></div>', unsafe_allow_html=True)

    st.markdown("<br><h3 style='text-align:center; color:white;'>🚀 Market Overview</h3>", unsafe_allow_html=True)

    # Market Indices (Nifty, BankNifty, Sensex)
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown('<div class="glass-card">NIFTY 50<div class="metric-val">22,300</div><div class="metric-down">▼ -1.2%</div></div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown('<div class="glass-card">BANKNIFTY<div class="metric-val">48,200</div><div class="metric-down">▼ -0.8%</div></div>', unsafe_allow_html=True)
    with col_m3:
        st.markdown('<div class="glass-card">SENSEX<div class="metric-val">73,500</div><div class="metric-down">▼ -1.0%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 0.5, 1])
    with btn_col:
        if st.button("🚀 Start Analysis Now"):
            st.session_state["start_app"] = True
            st.rerun()
    st.stop()

# =========================
# 📊 DASHBOARD (Dates Clear Dikhengi)
# =========================
st.markdown("<h2 style='color:white;'>📊 Analysis Dashboard</h2>", unsafe_allow_html=True)

# Sidebar setup (wahi rahega)
sector_stocks = {
    "IT": {"TCS":"TCS.NS","Infosys":"INFY.NS"},
    "Banking": {"HDFC":"HDFCBANK.NS","SBI":"SBIN.NS"}
}
sector = st.sidebar.selectbox("Sector", list(sector_stocks.keys()))
stock = st.sidebar.selectbox("Stock", list(sector_stocks[sector].keys()))
symbol = sector_stocks[sector][stock]

df = yf.download(symbol, start=d.date(2023,1,1), end=d.date.today())

if not df.empty:
    # ARIMA Model Fitting
    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=15)
    future_dates = pd.date_range(df.index[-1], periods=16, freq='B')[1:]

    # Plotly Graph (Taki Dates saaf dikhein aur zoom ho sake)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Actual Price", line=dict(color='#2ecc71')))
    fig.add_trace(go.Scatter(x=future_dates, y=forecast, name="Forecast", line=dict(color='#e74c3c', dash='dash')))

    fig.update_layout(
        title=f"{stock} Price Forecast",
        xaxis_title="Date",
        yaxis_title="Price (INR)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )

    st.plotly_chart(fig, use_container_width=True)

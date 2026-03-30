import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Indian Stock Analysis Platform", layout="wide")

# --- Global CSS (Common for all pages) ---
st.markdown("""
<style>
/* PURE GLOBAL BACKGROUND - Har page par dikhega */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.85)),
    url("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?q=80&w=2070"); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Glassy Containers */
.glass-container {
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
}

/* Text & Title Styles */
.main-title {
    color: white;
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
.sub-title {
    color: #00d1ff;
    text-align: center;
    font-size: 20px;
    margin-bottom: 40px;
}

/* Metric Styling */
[data-testid="stMetricValue"] { color: #00ffcc !important; font-size: 32px !important; }
[data-testid="stMetricLabel"] { color: white !important; }

/* Login Box Custom Size */
.login-wrapper {
    max-width: 400px;
    margin: auto;
    margin-top: 50px;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0.7) !important;
}
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state.start_app = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# 🔐 LOGIN PAGE
# =========================
if not st.session_state.logged_in:
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align:center; color:white;">🔐 Member Login</h2>', unsafe_allow_html=True)
    st.write("---")
    
    option = st.radio("", ["Login", "Sign Up"], horizontal=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    users = {"admin": "1234", "chaitanya": "finance123"}
    
    if st.button("Access Dashboard", use_container_width=True):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state.start_app:
    st.markdown('<h1 class="main-title">🚀 Indian Stock Analysis Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Predict • Analyze • Grow your Wealth</p>', unsafe_allow_html=True)

    # Homepage Glass Cards
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="glass-container" style="text-align:center;"><h3>📊 Analysis</h3><p>Historical trends & patterns</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="glass-container" style="text-align:center;"><h3>🔮 Forecast</h3><p>AI-driven price predictions</p></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="glass-container" style="text-align:center;"><h3>⚡ Live</h3><p>Real-time index tracking</p></div>', unsafe_allow_html=True)

    st.write("##")
    
    # Market Overview
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:white; text-align:center;">Market Performance</h3>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("NIFTY 50", "22,300", "-1.2%")
    m2.metric("BANKNIFTY", "48,200", "-0.8%")
    m3.metric("SENSEX", "73,500", "-1.0%")
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("##")
    if st.button("🚀 Enter Analytics Dashboard", use_container_width=True):
        st.session_state.start_app = True
        st.rerun()
    st.stop()

# =========================
# 📊 DASHBOARD PAGE
# =========================
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.title("📈 Stock Analysis & Prediction")

st.sidebar.header("Control Panel")
stock_list = {"TCS": "TCS.NS", "Infosys": "INFY.NS", "Reliance": "RELIANCE.NS", "SBI": "SBIN.NS"}
selected_stock = st.sidebar.selectbox("Choose Company", list(stock_list.keys()))
forecast_days = st.sidebar.slider("Days to Forecast", 5, 30, 10)

# Fetching Data
df = yf.download(stock_list[selected_stock], start="2023-01-01")

if not df.empty:
    # Arima Model Logic
    model = ARIMA(df['Close'], order=(5,1,0)).fit()
    pred = model.forecast(steps=forecast_days)
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('none') # Transparent background for plot
    ax.set_facecolor('rgba(0,0,0,0.5)')
    ax.plot(df.index[-100:], df['Close'][-100:], label="Recent Price", color="#00d1ff", linewidth=2)
    
    # Future dates for forecast
    future_dates = pd.date_range(df.index[-1], periods=forecast_days+1)[1:]
    ax.plot(future_dates, pred, '--', color="#ff4b4b", label="Prediction")
    
    ax.tick_params(colors='white')
    ax.legend()
    st.pyplot(fig)
    
    st.subheader(f"Next {forecast_days} Days Forecast Data")
    st.dataframe(pd.DataFrame({"Predicted Price": pred.values}, index=future_dates.date), use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.start_app = False
    st.rerun()

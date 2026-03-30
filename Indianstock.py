import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Indian Stock Analysis Platform", layout="wide")

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state.start_app = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- CSS (Enhanced UI) ---
st.markdown("""
<style>
/* GLOBAL BACKGROUND */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
    url("https://images.unsplash.com/photo-1611974717483-5867ff43997f"); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* LOGIN BOX ENHANCEMENT */
.login-box {
    background: rgba(255,255,255,0.08);
    padding:35px;
    border-radius:20px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    width:380px;
    margin:auto;
    margin-top:20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    text-align: center;
}
.user-avatar {
    width: 80px;
    height: 80px;
    background: rgba(255,255,255,0.1);
    border-radius: 50%;
    margin: 0 auto 20px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* HOMEPAGE ELEMENTS */
.main-header { text-align: center; color: white; padding-top: 50px; font-weight: bold; }
.sub-header { text-align: center; color: #cccccc; font-size: 18px; margin-bottom: 40px; }

.card-container { display: flex; justify-content: center; gap: 20px; margin-bottom: 50px; flex-wrap: wrap; }
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 15px;
    padding: 30px;
    width: 280px;
    text-align: center;
    color: white;
}
.card-icon { font-size: 40px; margin-bottom: 15px; }

/* DASHBOARD OVERLAY */
.dashboard-container {
    background: rgba(0, 0, 0, 0.6);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* METRICS & TEXT */
[data-testid="stMetricValue"] { color: white !important; font-size: 28px !important; font-weight: bold !important; }
.stTitle { color: white !important; font-weight: bold !important; }
label { color: #dddddd !important; font-weight: 500 !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN SYSTEM
# =========================
if not st.session_state.logged_in:
    st.markdown('<div class="center-title" style="text-align:center; margin-top:80px; color:white; font-size:32px; font-weight:bold;">🇮🇳 Welcome to Indian Stock Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    # Login Image/Icon
    st.markdown('<div class="user-avatar">👤</div>', unsafe_allow_html=True)
    
    option = st.radio("", ["Login", "Sign Up", "Forgot Password"])
    username = st.text_input("Username")
    password = ""
    if option != "Forgot Password":
        password = st.text_input("Password", type="password")

    users = {"admin": "1234", "chaitanya": "finance123", "demo": "demo123"}
    error = ""

    if option == "Login":
        if st.button("Access Account", use_container_width=True):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                error = "Invalid username or password"
    elif option == "Sign Up":
        if st.button("Create Account", use_container_width=True): st.success("Account created!")
    
    if error:
        st.markdown(f'<div style="color:#ff6b6b; margin-top:10px;">{error}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state.start_app:
    st.markdown('<h1 class="main-header">🚀 Indian Stock Analysis Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Predict • Analyze • Grow your Wealth 📊</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <div class="glass-card">
            <div class="card-icon">📊</div>
            <div class="card-title">Stock Analysis</div>
            <div class="card-desc">Deep dive into historical movements.</div>
        </div>
        <div class="glass-card">
            <div class="card-icon">🔮</div>
            <div class="card-title">Forecasting</div>
            <div class="card-desc">Predict trends with ARIMA models.</div>
        </div>
        <div class="glass-card">
            <div class="card-icon">⚡</div>
            <div class="card-title">Live Data</div>
            <div class="card-desc">Real-time market tracking.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center; color:white; font-size:22px; margin-bottom:20px;">🚀 Market Overview</div>', unsafe_allow_html=True)
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("NIFTY 50", "22,300", "-1.2%")
    m_col2.metric("BANKNIFTY", "48,200", "-0.8%")
    m_col3.metric("SENSEX", "73,500", "-1.0%")

    st.write("##")
    c1, c2, c3 = st.columns([1.5, 1, 1.5])
    with c2:
        if st.button("🚀 Enter Dashboard", use_container_width=True):
            st.session_state.start_app = True
            st.rerun()
    st.stop()

# =========================
# 📊 DASHBOARD
# =========================
# Wrap everything in a glass container for visibility against the background
st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)

st.title("📊 Analysis Dashboard")

st.sidebar.header("Settings")
start_date = st.sidebar.date_input("Start Date", d.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", d.date.today())
forecast_days = st.sidebar.slider("Forecast Days", 5, 60, 10)

stocks = {"TCS": "TCS.NS", "Infosys": "INFY.NS", "Reliance": "RELIANCE.NS", "SBI": "SBIN.NS", "HDFC Bank": "HDFCBANK.NS"}
stock = st.sidebar.selectbox("Select Stock", list(stocks.keys()))
symbol = stocks[stock]

df = yf.download(symbol, start=start_date, end=end_date)

if not df.empty:
    df = df[['Close']]
    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_days)
    future_dates = pd.date_range(df.index[-1], periods=forecast_days+1, freq='B')[1:]

    # Visualizing Graph
    fig, ax = plt.subplots(figsize=(10,4))
    # Dark mode graph styling
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#1e1e1e')
    ax.plot(df.index, df['Close'], color='#00d1ff', label="Actual")
    ax.plot(future_dates, forecast, color='#ff4b4b', linestyle='--', label="Forecast")
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.legend()
    st.pyplot(fig)

    st.dataframe(pd.DataFrame({"Forecast Price": forecast.values}, index=future_dates.date), use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.start_app = False
    st.rerun()

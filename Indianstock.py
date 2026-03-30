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

# --- CSS (Updated to match Image) ---
st.markdown("""
<style>
.stApp {
    /* --- ATTRACTIVE STOCK BACKGROUND IMAGE --- */
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
    url("https://images.unsplash.com/photo-1611974717483-5867ff43997f"); 
    /* Agar niche wali pasand na aaye toh upar wali line uncomment karein (pehle '#' hatayein) aur niche wali ko # se block karein */
    /* url("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f"); */
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Homepage Header */
.main-header {
    text-align: center;
    color: white;
    padding-top: 50px;
    font-weight: bold;
}
.sub-header {
    text-align: center;
    color: #cccccc;
    font-size: 18px;
    margin-bottom: 40px;
}

/* Glass Cards */
.card-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 50px;
    flex-wrap: wrap; /* responsive on small screens */
}
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 15px;
    padding: 30px;
    width: 280px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}
.card-icon { font-size: 40px; margin-bottom: 15px; }
.card-title { font-weight: bold; font-size: 20px; margin-bottom: 8px; }
.card-desc { font-size: 14px; color: #aaaaaa; line-height: 1.4; }

/* Market Metric Section */
.market-section {
    text-align: center;
    color: white;
    font-size: 22px;
    font-weight: 500;
    margin-bottom: 25px;
}

/* Metric Styling */
[data-testid="stMetricLabel"] { color: #dddddd !important; font-size: 16px !important;}
[data-testid="stMetricValue"] { color: white !important; font-size: 28px !important; font-weight: bold !important; }
[data-testid="stMetricDelta"] svg { fill: #ff4b4b !important; }
[data-testid="stMetricDelta"] div { color: #ff4b4b !important; font-weight: bold !important;}


/* Login Box */
.login-box {
    background: rgba(255,255,255,0.08);
    padding:35px;
    border-radius:20px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    width:380px;
    margin:auto;
    margin-top:50px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}
.center-title {
    text-align:center;
    margin-top:80px;
    color:white;
    font-size:32px;
    font-weight:bold;
}
.error { color:#ff6b6b; font-size:15px; text-align:center; margin-top:12px; font-weight:500; }

/* Custom Styling for Streamlit Buttons to look better on this background */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN SYSTEM
# =========================
if not st.session_state.logged_in:
    st.markdown('<div class="center-title">🇮🇳 Welcome to Indian Stock Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    option = st.radio("", ["Login", "Sign Up", "Forgot Password"])
    username = st.text_input("Username")
    password = ""
    if option != "Forgot Password":
        password = st.text_input("Password", type="password")

    users = {"admin": "1234", "chaitanya": "finance123", "demo": "demo123"}
    error = ""

    if option == "Login":
        # Centering the login button a bit more
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("Login", use_container_width=True):
                if username in users and users[username] == password:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    error = "Invalid username or password"
    elif option == "Sign Up":
         c1, c2, c3 = st.columns([1, 2, 1])
         with c2:
            if st.button("Create Account", use_container_width=True): st.success("Account created (Demo Only)")
    elif option == "Forgot Password":
         c1, c2, c3 = st.columns([1, 2, 1])
         with c2:
            if st.button("Recover Password", use_container_width=True):
                if username in users: st.info(f"Your password is: {users[username]}")
                else: error = "User not found"

    if error:
        st.markdown(f'<div class="error">{error}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 HOMEPAGE (UPDATED TO MATCH IMAGE)
# =========================
if not st.session_state.start_app:
    # Title Section
    st.markdown('<h1 class="main-header">🚀 Indian Stock Analysis Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Predict • Analyze • Grow your Wealth 📊</p>', unsafe_allow_html=True)

    # Glass Cards Section
    st.markdown("""
    <div class="card-container">
        <div class="glass-card">
            <div class="card-icon">📊</div>
            <div class="card-title">Stock Analysis</div>
            <div class="card-desc">Dive deep into historical price movements and technical indicators.</div>
        </div>
        <div class="glass-card">
            <div class="card-icon">🔮</div>
            <div class="card-title">Forecasting</div>
            <div class="card-desc">Utilize advanced ARIMA models to predict future price trends.</div>
        </div>
        <div class="glass-card">
            <div class="card-icon">⚡</div>
            <div class="card-title">Live Data</div>
            <div class="card-desc">Get near real-time updates from major Indian indices and stocks.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Market Overview Section
    st.markdown('<div class="market-section">🚀 Market Overview</div>', unsafe_allow_html=True)
    
    # Adding some padding for metrics
    st.write("#")
    m_col1, m_col2, m_col3 = st.columns([1,1,1])
    with m_col1:
        st.metric("NIFTY 50", "22,300", "-1.2%")
    with m_col2:
        st.metric("BANKNIFTY", "48,200", "-0.8%")
    with m_col3:
        st.metric("SENSEX", "73,500", "-1.0%")

    # Start Button
    st.write("##")
    st.write("##")
    c1, c2, c3 = st.columns([1.5, 1, 1.5])
    with c2:
        # Green-ish button to stand out
        if st.button("🚀 Start Analysis Now", use_container_width=True, type="primary"):
            st.session_state.start_app = True
            st.rerun()

    st.stop()

# =========================
# 📊 DASHBOARD (UNCHANGED)
# =========================
st.title("📊 Indian Stock Analysis Dashboard")
st.sidebar.header("Settings")

start_date = st.sidebar.date_input("Start Date", d.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", d.date.today())
forecast_days = st.sidebar.slider("Forecast Days", 5, 60, 10)

stocks = {
    "TCS": "TCS.NS", "Infosys": "INFY.NS", "Wipro": "WIPRO.NS", "HCL Tech": "HCLTECH.NS", "Tech Mahindra": "TECHM.NS",
    "HDFC Bank": "HDFCBANK.NS", "ICICI Bank": "ICICIBANK.NS", "SBI": "SBIN.NS", "Axis Bank": "AXISBANK.NS", "Kotak Bank": "KOTAKBANK.NS",
    "ITC": "ITC.NS", "HUL": "HINDUNILVR.NS", "Nestle India": "NESTLEIND.NS", "Britannia": "BRITANNIA.NS", "Dabur": "DABUR.NS",
    "Reliance": "RELIANCE.NS", "ONGC": "ONGC.NS", "NTPC": "NTPC.NS", "Power Grid": "POWERGRID.NS", "Coal India": "COALINDIA.NS",
    "Maruti Suzuki": "MARUTI.NS", "Tata Motors": "TATAMOTORS.NS", "M&M": "M&M.NS", "Bajaj Auto": "BAJAJ-AUTO.NS", "Hero MotoCorp": "HEROMOTOCO.NS"
}

stock = st.sidebar.selectbox("Select Stock", list(stocks.keys()))
symbol = stocks[stock]

df = yf.download(symbol, start=start_date, end=end_date)

if not df.empty:
    df = df[['Close']]
    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_days)
    future_dates = pd.date_range(df.index[-1], periods=forecast_days+1, freq='B')[1:]

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df.index, df['Close'], label="Actual Price")
    ax.plot(future_dates, forecast, '--', label="Forecast")
    ax.set_title(f"{stock} Price Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    fig.autofmt_xdate()
    ax.legend()
    st.pyplot(fig)
    st.dataframe(pd.DataFrame({"Forecast": forecast.values}, index=future_dates))

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.start_app = False
    st.rerun()

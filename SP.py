import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import sqlite3
import plotly.graph_objects as go

# ---------------- CONFIG & THEME ----------------
st.set_page_config(page_title="Stock Sense Analytics | AI Pro", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium Dark UI
st.markdown("""
<style>
    /* Main Background with Stock Market Visual */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1611974717482-58a00f244532?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Glassmorphism Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00d4ff;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 60px;
        font-weight: 800;
        background: -webkit-linear-gradient(#00d4ff, #0055ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 20, 0.95);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)")
    conn.commit()
    return conn, c

conn, c = init_db()

# ---------------- SESSION MANAGEMENT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- NAVIGATION ----------------
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# ---------------- HOME PAGE ----------------
if st.session_state.page == "home" and not st.session_state.logged_in:
    st.markdown('<h1 class="main-title">STOCK SENSE ANALYTICS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#aaa; font-size:20px;">Master the Market with AI-Powered Precision</p>', unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><h3>📈 Real-Time Data</h3><p>Live feeds from NSE/BSE using advanced API integration.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>🤖 ARIMA Forecasting</h3><p>Proprietary AI models to predict future price movements.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>📊 Pro Dashboards</h3><p>Interactive charts designed for modern day traders.</p></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Entrance Buttons
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        btn_col1, btn_col2 = st.columns(2)
        if btn_col1.button("🚀 Access Dashboard", use_container_width=True):
            navigate_to("login")
        if btn_col2.button("📝 Join the Network", use_container_width=True):
            navigate_to("signup")

# ---------------- LOGIN & SIGNUP ----------------
if st.session_state.page == "login" and not st.session_state.logged_in:
    st.markdown('<h2 style="text-align:center;">🔐 Secure Portal</h2>', unsafe_allow_html=True)
    with st.container():
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login Now", use_container_width=True):
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pw))
            if c.fetchone():
                st.session_state.logged_in = True
                navigate_to("dashboard")
            else:
                st.error("Invalid credentials.")
        if st.button("← Back to Home"): navigate_to("home")

if st.session_state.page == "signup" and not st.session_state.logged_in:
    st.markdown('<h2 style="text-align:center;">📝 Create Account</h2>', unsafe_allow_html=True)
    new_user = st.text_input("Choose Username")
    new_pw = st.text_input("Create Password", type="password")
    if st.button("Register"):
        try:
            c.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_pw))
            conn.commit()
            st.success("Registration Complete! Please login.")
            navigate_to("login")
        except:
            st.error("Username already taken.")

# ---------------- DASHBOARD (PRO) ----------------
if st.session_state.logged_in:
    st.sidebar.title("💎 Pro Panel")
    
    # Sector & Stock Data (Expanded)
    sector_stocks = {
        "IT": {"TCS":"TCS.NS", "INFY":"INFY.NS", "WIPRO":"WIPRO.NS", "HCL":"HCLTECH.NS"},
        "Banking": {"HDFC":"HDFCBANK.NS", "SBI":"SBIN.NS", "ICICI":"ICICIBANK.NS", "AXIS":"AXISBANK.NS"},
        "Energy": {"Reliance":"RELIANCE.NS", "Adani Green":"ADANIGREEN.NS", "Tata Power":"TATAPOWER.NS"},
        "Auto": {"Tata Motors":"TATAMOTORS.NS", "Mahindra":"M&M.NS", "Maruti":"MARUTI.NS"}
    }
    
    selected_sector = st.sidebar.selectbox("Market Sector", list(sector_stocks.keys()))
    selected_stock = st.sidebar.selectbox("Select Asset", list(sector_stocks[selected_sector].keys()))
    symbol = sector_stocks[selected_sector][selected_stock]
    
    f_days = st.sidebar.slider("Forecast Horizon (Days)", 5, 60, 15)
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        navigate_to("home")

    # --- Main Dashboard Content ---
    st.markdown(f"## 📊 Analyzing: {selected_stock} ({symbol})")
    
    # Fetch Data
    data = yf.download(symbol, period="2y")
    
    if not data.empty:
        # Layout Columns
        m1, m2, m3 = st.columns(3)
        current_price = data['Close'].iloc[-1].item() # Fixing float extraction
        prev_price = data['Close'].iloc[-2].item()
        change = current_price - prev_price
        
        m1.metric("Current Price", f"₹{current_price:,.2f}", f"{change:,.2f}")
        m2.metric("52W High", f"₹{data['High'].max().item():,.2f}")
        m3.metric("52W Low", f"₹{data['Low'].min().item():,.2f}")

        # Modern Chart using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Historical Price", line=dict(color='#00d4ff', width=2)))
        
        # ARIMA Model Logic
        try:
            model = ARIMA(data['Close'], order=(5,1,0))
            model_fit = model.fit()
            forecast_values = model_fit.forecast(steps=f_days)
            future_dates = pd.date_range(data.index[-1], periods=f_days+1, freq='B')[1:]
            
            fig.add_trace(go.Scatter(x=future_dates, y=forecast_values, name="AI Prediction", line=dict(color='#ffaa00', dash='dot')))
        except:
            st.warning("Prediction model is calculating...")

        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        # Data View
        with st.expander("📂 View Raw Market Data"):
            st.dataframe(data.tail(10), use_container_width=True)

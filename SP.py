import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, date, timedelta
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go
import sqlite3

# --- PAGE CONFIG ---
st.set_page_config(page_title="Stock Sense Pro | AI Analytics", layout="wide")

# --- DATABASE & AUTH LOGIC ---
conn = sqlite3.connect("users_pro.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, email TEXT)")
conn.commit()

# --- CSS: PREMIUM UI & BACKGROUND ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), 
                    url("https://images.unsplash.com/photo-1611974717482-58a00f244532?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    .main-header {
        font-size: 55px; font-weight: 800; text-align: center;
        background: -webkit-linear-gradient(#00fbff, #0072ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3em;
        background-color: #0072ff; color: white; border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "auth_status" not in st.session_state: st.session_state.auth_status = False
if "page" not in st.session_state: st.session_state.page = "Home"

# --- NAVBAR (TOP CORNER STYLE) ---
with st.container():
    col_t1, col_t2, col_t3, col_t4 = st.columns([5, 1, 1, 1])
    with col_t1: st.write(f"📅 **Date:** {date.today()} | 🕒 **Time:** {datetime.now().strftime('%H:%M:%S')}")
    with col_t2: 
        if st.button("🏠 Home"): st.session_state.page = "Home"
    with col_t3:
        if not st.session_state.auth_status:
            if st.button("🔐 Login"): st.session_state.page = "Login"
        else: st.write("✅ Active")
    with col_t4:
        if not st.session_state.auth_status:
            if st.button("📝 Join"): st.session_state.page = "Signup"
        else:
            if st.button("🚪 Logout"): 
                st.session_state.auth_status = False
                st.rerun()

# --- AUTH PAGES ---
if st.session_state.page == "Login":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Login to Stock Sense")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Sign In"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pw))
        if c.fetchone():
            st.session_state.auth_status = True
            st.session_state.page = "Dashboard"
            st.rerun()
        else: st.error("Wrong credentials")
    if st.button("Forgot Password?"): st.info("Password recovery sent to registered email (Simulated)")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

if st.session_state.page == "Signup":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_email = st.text_input("Email")
    new_pw = st.text_input("Password", type="password")
    if st.button("Register"):
        try:
            c.execute("INSERT INTO users VALUES (?,?,?)", (new_user, new_pw, new_email))
            conn.commit()
            st.success("Account created! Go to Login.")
        except: st.error("Username exists")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- HOME PAGE ---
if st.session_state.page == "Home":
    st.markdown('<h1 class="main-header">STOCK SENSE ANALYTICS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:gray;">Advanced AI Time-Series Forecasting for Traders</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="glass-card"><h3>Short Term</h3><p>7-Day Micro Trends</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="glass-card"><h3>Mid Term</h3><p>30-Day Cyclical Shifts</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="glass-card"><h3>Long Term</h3><p>90-Day Structural Forecasts</p></div>', unsafe_allow_html=True)
    st.stop()

# --- DASHBOARD (AFTER LOGIN) ---
if st.session_state.auth_status:
    # 25-30 Stocks per Sector (Sample set for space, easily expandable)
    sectors = {
        "IT/Tech": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS", "LTIM.NS", "MPHASIS.NS", "COFORGE.NS", "PERSISTENT.NS", "KPITTECH.NS", "BSOFT.NS", "ZENSARTECH.NS", "LTTS.NS", "SONATAWSOFT.NS", "TATAELXSI.NS"],
        "Banking/Finance": ["HDFCBANK.NS", "SBIN.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "INDUSINDBK.NS", "PNB.NS", "BANKBARODA.NS", "CANBK.NS", "IDFCFIRSTB.NS", "FEDERALBNK.NS", "YESBANK.NS", "AUBANK.NS", "BANDHANBNK.NS", "RBLBANK.NS"],
        "Energy/Power": ["RELIANCE.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "BPCL.NS", "IOC.NS", "TATAPOWER.NS", "ADANIGREEN.NS", "ADANIPOWER.NS", "SUZLON.NS", "NHPC.NS", "GAIL.NS", "JSWENERGY.NS", "SJVN.NS"]
    }

    st.sidebar.header("🎯 Market Analysis")
    sec_choice = st.sidebar.selectbox("Select Sector", list(sectors.keys()))
    stock_choice = st.sidebar.selectbox("Select Stock", sectors[sec_choice])
    
    # Forecasting Horizon Selection
    term = st.sidebar.radio("Forecasting Horizon", ["Short Term (7D)", "Mid Term (30D)", "Long Term (90D)"])
    days_map = {"Short Term (7D)": 7, "Mid Term (30D)": 30, "Long Term (90D)": 90}
    horizon = days_map[term]

    # Data Fetching
    data = yf.download(stock_choice, start="2022-01-01", end=date.today())
    
    if not data.empty:
        # Layout
        col_main, col_metrics = st.columns([3, 1])
        
        with col_main:
            st.subheader(f"Price Analysis: {stock_choice}")
            
            # ARIMA Model Fit
            model = ARIMA(data['Close'], order=(5,1,0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=horizon)
            future_dates = pd.date_range(data.index[-1], periods=horizon+1, freq='B')[1:]

            # Plotly Visualization
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index[-100:], y=data['Close'][-100:], name="Recent Price", line=dict(color="#00fbff")))
            fig.add_trace(go.Scatter(x=future_dates, y=forecast, name=f"{term} AI Forecast", line=dict(color="#ff9100", dash='dot')))
            
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col_metrics:
            st.subheader("Key Statistics")
            current = data['Close'].iloc[-1].item()
            st.metric("LTP (Last Traded)", f"₹{current:,.2f}")
            st.metric("Expected Price", f"₹{forecast.iloc[-1]:,.2f}")
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.write("**Analysis Note:**")
            st.write(f"The {term} model suggests a potential trend towards {forecast.iloc[-1]:,.2f}. Always use stop-losses.")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("Data not available for this ticker.")

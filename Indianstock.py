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

# --- CSS (MATCHED TO YOUR SCREENSHOT) ---
st.markdown("""
<style>
/* Background Setup */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), 
                url("https://images.unsplash.com/photo-1611974717483-5867ff43997f?q=80&w=2000&auto=format&fit=crop"); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Glassmorphism Login Box */
.login-box {
    background: rgba(255, 255, 255, 0.03); 
    padding: 40px;
    border-radius: 12px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    width: 100%;
    max-width: 450px;
    margin: auto;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    color: white;
}

/* Welcome Title (Matched to Screenshot) */
.welcome-header {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px 25px;
    border-radius: 15px;
    display: inline-block;
    color: white;
    font-weight: bold;
    font-size: 20px;
    margin-bottom: 30px;
    backdrop-filter: blur(5px);
}

.center-container {
    text-align: center;
    margin-top: 50px;
}

/* Input Fields & Labels */
label {
    color: #ffffff !important;
    font-weight: 500 !important;
}

div[data-baseweb="input"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px !important;
}

input {
    color: white !important;
}

/* Error Message (Matched to Screenshot) */
.error-msg {
    background: rgba(255, 75, 75, 0.15);
    border: 1px solid #ff4b4b;
    padding: 10px;
    border-radius: 5px;
    color: #ff6b6b;
    font-size: 14px;
    margin-top: 20px;
    text-align: left;
}

/* Buttons */
.stButton > button {
    background-color: #2c2c2e !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    transition: 0.3s;
}
.stButton > button:hover {
    background-color: #3a3a3c !important;
    border-color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN SYSTEM
# =========================
if not st.session_state.logged_in:
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.markdown('<div class="welcome-header">IN Welcome to INDIA STOCK ANALYSIS</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    
    option = st.radio("", ["Login", "Sign Up", "Forgot Password"], horizontal=False)
    username = st.text_input("Username")
    password = ""
    if option != "Forgot Password":
        password = st.text_input("Password", type="password")

    users = {"admin": "1234", "chaitanya": "finance123", "demo": "demo123"}
    error = ""

    if st.button("Login", use_container_width=True):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            error = "Invalid Credentials"

    if error:
        st.markdown(f'<div class="error-msg">{error}</div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 HOMEPAGE & DASHBOARD
# =========================
if not st.session_state.start_app:
    st.markdown('<h1 style="text-align:center; color:white;">🚀 Indian Stock Analysis Platform</h1>', unsafe_allow_html=True)
    
    # Simple Metrics and Cards
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("NIFTY 50", "22,300", "-1.2%")
    with c2: st.metric("BANKNIFTY", "48,200", "-0.8%")
    with c3: st.metric("SENSEX", "73,500", "-1.0%")

    if st.button("🚀 Start Analysis Now", type="primary"):
        st.session_state.start_app = True
        st.rerun()
    st.stop()

# --- Dashboard View ---
st.title("📊 Indian Stock Analysis Dashboard")
# ... (Baki ka ARIMA logic jo pehle tha wahi rahega)

import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Sense Analytics", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- CSS (MATCH IMAGE UI) ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
    url("https://images.unsplash.com/photo-1504384308090-c894fdcc538d");
    background-size: cover;
}

.title {
    text-align:center;
    color:white;
    font-size:50px;
    font-weight:700;
}

.subtitle {
    text-align:center;
    color:#bbb;
    margin-bottom:30px;
}

.card {
    background: rgba(255,255,255,0.08);
    padding:25px;
    border-radius:18px;
    text-align:center;
    color:white;
    backdrop-filter: blur(10px);
}

.box {
    background: rgba(255,255,255,0.1);
    padding:25px;
    border-radius:18px;
    color:white;
    backdrop-filter: blur(15px);
}

.nav button {
    width:100%;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"
with c2:
    if st.button("ℹ️ About"):
        st.session_state.page = "about"
with c3:
    if st.button("🔐 Login"):
        st.session_state.page = "login"

# ---------------- HOME ----------------
if st.session_state.page == "home" and not st.session_state.logged_in:

    st.markdown('<div class="title">🚀 Stock Sense Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart AI-Based Stock Prediction Platform</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card">📊<br><b>Analyze Stocks</b><br>Deep insights</div>', unsafe_allow_html=True)
    c2.markdown('<div class="card">🔮<br><b>Forecast Prices</b><br>AI prediction</div>', unsafe_allow_html=True)
    c3.markdown('<div class="card">⚡<br><b>Live Data</b><br>Real-time</div>', unsafe_allow_html=True)

    st.markdown("### 📍 Why Use This App?")
    st.write("""
    ✔ Real-time Indian stock market  
    ✔ AI forecasting (ARIMA)  
    ✔ Sector analysis  
    ✔ Beginner friendly  
    """)

    # ---- Bottom Split (About + Login preview) ----
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="box"><h3>About This App</h3>', unsafe_allow_html=True)
        st.write("""
        ✔ Live Market Data  
        ✔ ARIMA Forecasting  
        ✔ Sector Analysis  
        👨‍💻 By Chaitanya Torankar  
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="box"><h3>Login to Continue</h3>', unsafe_allow_html=True)
        st.write("Go to Login page to access dashboard")
        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ---------------- ABOUT ----------------
if st.session_state.page == "about" and not st.session_state.logged_in:

    st.markdown('<div class="title">ℹ️ About</div>', unsafe_allow_html=True)

    st.markdown("""
    ### 📊 Stock Sense Analytics

    - Live Indian Market Data  
    - Forecast using ARIMA Model  
    - Interactive Dashboard  

    ### 🧠 Tech:
    Python, Streamlit, Pandas, yFinance  

    👨‍💻 Developed by Chaitanya
    """)

    st.stop()

# ---------------- LOGIN ----------------
if st.session_state.page == "login" and not st.session_state.logged_in:

    st.markdown('<div class="title">🔐 Login</div>', unsafe_allow_html=True)

    users = {"admin":"1234", "chaitanya":"finance123"}

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# ---------------- DASHBOARD ----------------
st.title("📊 Stock Dashboard")

start = st.sidebar.date_input("Start", d.date(2022,1,1))
end = st.sidebar.date_input("End", d.date.today())

stocks = {
    "Reliance":"RELIANCE.NS",
    "TCS":"TCS.NS",
    "Infosys":"INFY.NS"
}

stock = st.sidebar.selectbox("Stock", list(stocks.keys()))
symbol = stocks[stock]

df = yf.download(symbol, start=start, end=end)

if not df.empty:
    df = df[['Close']]

    model = ARIMA(df['Close'], order=(5,1,0))
    fit = model.fit()
    forecast = fit.forecast(steps=30)

    future_dates = pd.date_range(df.index[-1], periods=31, freq='B')[1:]

    fig, ax = plt.subplots()
    ax.plot(df.index, df['Close'], label="Actual")
    ax.plot(future_dates, forecast, '--', label="Forecast")
    ax.legend()

    st.pyplot(fig)

# ---------------- LOGOUT ----------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.page = "home"
    st.rerun()

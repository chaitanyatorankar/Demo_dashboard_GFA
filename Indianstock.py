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

# ---------------- CSS ----------------
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

# =========================
# 📊 DASHBOARD
# =========================

st.title("📊 Stock Dashboard")

st.sidebar.header("Settings")

start_date = st.sidebar.date_input("Start Date", d.date(2022,1,1))
end_date = st.sidebar.date_input("End Date", d.date.today())

forecast_days = st.sidebar.slider("Forecast Days", 5, 90, 30)

# ✅ BIGGER STOCK LIST (15+ each)
sector_stocks = {
    "IT": {
        "TCS":"TCS.NS","Infosys":"INFY.NS","Wipro":"WIPRO.NS",
        "HCL Tech":"HCLTECH.NS","Tech Mahindra":"TECHM.NS",
        "LTIMindtree":"LTIM.NS","Mphasis":"MPHASIS.NS",
        "Coforge":"COFORGE.NS","L&T Tech":"LTTS.NS",
        "Zensar":"ZENSARTECH.NS","Persistent":"PERSISTENT.NS",
        "KPIT":"KPITTECH.NS","Birlasoft":"BSOFT.NS",
        "Tanla":"TANLA.NS","Route Mobile":"ROUTE.NS"
    },

    "Banking": {
        "HDFC Bank":"HDFCBANK.NS","ICICI":"ICICIBANK.NS","SBI":"SBIN.NS",
        "Axis":"AXISBANK.NS","Kotak":"KOTAKBANK.NS",
        "IndusInd":"INDUSINDBK.NS","Yes Bank":"YESBANK.NS",
        "IDFC First":"IDFCFIRSTB.NS","Bandhan":"BANDHANBNK.NS",
        "PNB":"PNB.NS","Bank of Baroda":"BANKBARODA.NS",
        "Canara":"CANBK.NS","Union Bank":"UNIONBANK.NS",
        "RBL":"RBLBANK.NS","Federal":"FEDERALBNK.NS"
    },

    "FMCG": {
        "ITC":"ITC.NS","HUL":"HINDUNILVR.NS","Nestle":"NESTLEIND.NS",
        "Britannia":"BRITANNIA.NS","Dabur":"DABUR.NS",
        "Godrej":"GODREJCP.NS","Marico":"MARICO.NS",
        "Colgate":"COLPAL.NS","Tata Consumer":"TATACONSUM.NS",
        "UBL":"UBL.NS","Emami":"EMAMILTD.NS",
        "Radico":"RADICO.NS","VBL":"VBL.NS",
        "Balrampur":"BALRAMCHIN.NS","Zydus Wellness":"ZYDUSWELL.NS"
    },

    "Energy": {
        "Reliance":"RELIANCE.NS","ONGC":"ONGC.NS","NTPC":"NTPC.NS",
        "Power Grid":"POWERGRID.NS","Coal India":"COALINDIA.NS",
        "BPCL":"BPCL.NS","HPCL":"HPCL.NS",
        "IOC":"IOC.NS","Adani Green":"ADANIGREEN.NS",
        "Adani Power":"ADANIPOWER.NS","Tata Power":"TATAPOWER.NS",
        "Torrent":"TORNTPOWER.NS","NHPC":"NHPC.NS",
        "Suzlon":"SUZLON.NS","GAIL":"GAIL.NS"
    },

    "Auto": {
        "Maruti":"MARUTI.NS","Tata Motors":"TATAMOTORS.NS",
        "M&M":"M&M.NS","Bajaj Auto":"BAJAJ-AUTO.NS",
        "Hero":"HEROMOTOCO.NS","Ashok Leyland":"ASHOKLEY.NS",
        "TVS":"TVSMOTOR.NS","Eicher":"EICHERMOT.NS",
        "Escorts":"ESCORTS.NS","Force Motors":"FORCEMOT.NS",
        "Sona BLW":"SONACOMS.NS","Exide":"EXIDEIND.NS",
        "Amara Raja":"AMARAJABAT.NS","Bosch":"BOSCHLTD.NS",
        "MRF":"MRF.NS"
    }
}

sector = st.sidebar.selectbox("Sector", list(sector_stocks.keys()))
stock = st.sidebar.selectbox("Stock", list(sector_stocks[sector].keys()))
symbol = sector_stocks[sector][stock]

df = yf.download(symbol, start=start_date, end=end_date)

if not df.empty:
    df = df[['Close']]

    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=forecast_days)

    future_dates = pd.date_range(df.index[-1], periods=forecast_days+1, freq='B')[1:]

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df.index, df['Close'], label="Actual")
    ax.plot(future_dates, forecast, '--', label="Forecast")

    ax.set_title(f"{stock} Forecast")
    ax.legend()

    st.pyplot(fig)

    st.dataframe(pd.DataFrame({"Forecast": forecast.values}, index=future_dates))

# LOGOUT
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["start_app"] = False
    st.rerun()

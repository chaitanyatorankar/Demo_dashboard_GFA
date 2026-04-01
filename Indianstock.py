import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="India Finance Analysis", layout="wide")

# --- Session State ---
if "start_app" not in st.session_state:
    st.session_state["start_app"] = False
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "portfolio" not in st.session_state:
    st.session_state["portfolio"] = []

# --- CSS ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
    url("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f");
    background-size: cover;
    background-attachment: fixed;
    overflow-x: hidden;
}
.title {text-align:center;color:white;font-size:44px;margin-top:40px;font-weight:700;}
.subtitle {text-align:center;color:#aaa;margin-bottom:30px;}
.card {
    background: rgba(255,255,255,0.08);
    padding:25px;border-radius:18px;text-align:center;color:white;
    transition:0.3s;
}
.card:hover {transform: scale(1.05);background: rgba(255,255,255,0.15);}
.login-box {
    background: rgba(255,255,255,0.1);
    padding:35px;border-radius:20px;
    backdrop-filter: blur(15px);
    width:350px;margin:auto;margin-top:40px;
    box-shadow: 0 0 25px rgba(0,0,0,0.25);
}
.stButton>button {
    background: linear-gradient(45deg,#00ffcc,#0099ff);
    color:black;border-radius:10px;font-weight:bold;
}
.about {
    background: rgba(255,255,255,0.05);
    padding:25px;border-radius:15px;color:#ddd;margin-top:30px;
}
.signal-buy {
    padding:15px;
    background:#0f5132;
    border-radius:10px;
    color:white;
    font-weight:600;
}
.signal-sell {
    padding:15px;
    background:#842029;
    border-radius:10px;
    color:white;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN
# =========================
if not st.session_state["logged_in"]:
    st.markdown('<div class="title">🚀 Future Stock AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    option = st.radio("", ["Login", "Sign Up", "Forgot Password"])
    username = st.text_input("Username")
    password = ""

    if option != "Forgot Password":
        password = st.text_input("Password", type="password")

    users = {"admin": "1234", "chaitanya": "finance123", "demo": "demo123"}

    if option == "Login":
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid login")

    elif option == "Sign Up":
        if st.button("Create Account"):
            st.success("Account created (Demo)")

    elif option == "Forgot Password":
        if st.button("Recover"):
            if username in users:
                st.info(f"Password: {users[username]}")
            else:
                st.error("User not found")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 🏠 HOMEPAGE
# =========================
if not st.session_state["start_app"]:
    st.markdown('<div class="title">📈 Indian Stock Analysis Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict • Analyze • Grow your Wealth</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card">📊<br><b>Stock Analysis</b><br>Analyze historical data</div>', unsafe_allow_html=True)
    c2.markdown('<div class="card">🔮<br><b>Forecasting</b><br>Predict future prices</div>', unsafe_allow_html=True)
    c3.markdown('<div class="card">⚡<br><b>Live Data</b><br>Real-time updates</div>', unsafe_allow_html=True)

    st.markdown("## 📊 Market Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric("NIFTY 50", "22,300", "-1.2%")
    m2.metric("BANKNIFTY", "48,200", "-0.8%")
    m3.metric("SENSEX", "73,500", "-1.0%")

    st.markdown("""
    <div class="about">
    <h3>💡 About Platform</h3>
    AI-powered stock analysis with forecasting, trading signals, and portfolio tracking.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Analysis Now"):
        st.session_state["start_app"] = True
        st.rerun()

    st.stop()

# =========================
# 📊 DASHBOARD
# =========================
st.title("📊 Stock Dashboard")

start_date = st.sidebar.date_input("Start Date", d.date(2022, 1, 1))
end_date = st.sidebar.date_input("End Date", d.date.today())
forecast_days = st.sidebar.slider("Forecast Days", 5, 90, 30)

sector_stocks = {
    "IT": {
        "TCS": "TCS.NS", "Infosys": "INFY.NS", "Wipro": "WIPRO.NS",
        "HCL Tech": "HCLTECH.NS", "Tech Mahindra": "TECHM.NS",
        "LTIMindtree": "LTIM.NS", "Mphasis": "MPHASIS.NS",
        "Coforge": "COFORGE.NS", "L&T Tech": "LTTS.NS",
        "Zensar": "ZENSARTECH.NS", "Persistent": "PERSISTENT.NS",
        "KPIT": "KPITTECH.NS", "Birlasoft": "BSOFT.NS",
        "Tanla": "TANLA.NS", "Route Mobile": "ROUTE.NS"
    },
    "Banking": {
        "HDFC Bank": "HDFCBANK.NS", "ICICI": "ICICIBANK.NS", "SBI": "SBIN.NS",
        "Axis": "AXISBANK.NS", "Kotak": "KOTAKBANK.NS",
        "IndusInd": "INDUSINDBK.NS", "Yes Bank": "YESBANK.NS",
        "IDFC First": "IDFCFIRSTB.NS", "Bandhan": "BANDHANBNK.NS",
        "PNB": "PNB.NS", "Bank of Baroda": "BANKBARODA.NS",
        "Canara": "CANBK.NS", "Union Bank": "UNIONBANK.NS",
        "RBL": "RBLBANK.NS", "Federal": "FEDERALBNK.NS"
    },
    "FMCG": {
        "ITC": "ITC.NS", "HUL": "HINDUNILVR.NS", "Nestle": "NESTLEIND.NS",
        "Britannia": "BRITANNIA.NS", "Dabur": "DABUR.NS",
        "Godrej": "GODREJCP.NS", "Marico": "MARICO.NS",
        "Colgate": "COLPAL.NS", "Tata Consumer": "TATACONSUM.NS",
        "UBL": "UBL.NS", "Emami": "EMAMILTD.NS",
        "Radico": "RADICO.NS", "VBL": "VBL.NS",
        "Balrampur": "BALRAMCHIN.NS", "Zydus Wellness": "ZYDUSWELL.NS"
    },
    "Energy": {
        "Reliance": "RELIANCE.NS", "ONGC": "ONGC.NS", "NTPC": "NTPC.NS",
        "Power Grid": "POWERGRID.NS", "Coal India": "COALINDIA.NS",
        "BPCL": "BPCL.NS", "HPCL": "HPCL.NS",
        "IOC": "IOC.NS", "Adani Green": "ADANIGREEN.NS",
        "Adani Power": "ADANIPOWER.NS", "Tata Power": "TATAPOWER.NS",
        "Torrent": "TORNTPOWER.NS", "NHPC": "NHPC.NS",
        "Suzlon": "SUZLON.NS", "GAIL": "GAIL.NS"
    },
    "Auto": {
        "Maruti": "MARUTI.NS", "Tata Motors": "TATAMOTORS.NS",
        "M&M": "M&M.NS", "Bajaj Auto": "BAJAJ-AUTO.NS",
        "Hero": "HEROMOTOCO.NS", "Ashok Leyland": "ASHOKLEY.NS",
        "TVS": "TVSMOTOR.NS", "Eicher": "EICHERMOT.NS",
        "Escorts": "ESCORTS.NS", "Force Motors": "FORCEMOT.NS",
        "Sona BLW": "SONACOMS.NS", "Exide": "EXIDEIND.NS",
        "Amara Raja": "AMARAJABAT.NS", "Bosch": "BOSCHLTD.NS",
        "MRF": "MRF.NS"
    }
}

sector = st.sidebar.selectbox("Sector", list(sector_stocks.keys()))
stock = st.sidebar.selectbox("Stock", list(sector_stocks[sector].keys()))
symbol = sector_stocks[sector][stock]

with st.spinner("Fetching stock data..."):
    df = yf.download(symbol, start=start_date, end=end_date, progress=False)

if df.empty or "Close" not in df.columns:
    st.error("No data found for the selected stock.")
    st.stop()

df = df[["Close"]].dropna()

if len(df) < 20:
    st.warning("Not enough data to build a forecast. Please select a wider date range.")
    st.stop()

try:
    model = ARIMA(df["Close"], order=(5, 1, 0))
    model_fit = model.fit()
    forecast_raw = model_fit.forecast(steps=forecast_days)
except Exception as e:
    st.error("Forecast model could not be built for this stock/date range.")
    st.stop()

forecast_values = np.asarray(forecast_raw).reshape(-1)
future_dates = pd.date_range(df.index[-1], periods=forecast_days + 1, freq="B")[1:]
forecast_series = pd.Series(forecast_values, index=future_dates)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df.index, df["Close"], label="Actual")
ax.plot(forecast_series.index, forecast_series.values, "--", label="Forecast")
ax.set_title(f"{stock} Forecast")
ax.legend()
st.pyplot(fig)

st.dataframe(pd.DataFrame({"Forecast": forecast_series.values}, index=forecast_series.index))

# =========================
# 📢 AI SIGNAL
# =========================
st.subheader("📢 AI Signal")

predicted_price = float(forecast_series.iloc[-1])
last_price = float(df["Close"].iloc[-1])

if predicted_price > last_price:
    st.markdown(
        f"<div class='signal-buy'>🟢 BUY Signal<br>Last Price: ₹{last_price:.2f} | Predicted Price: ₹{predicted_price:.2f}</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"<div class='signal-sell'>🔴 SELL Signal<br>Last Price: ₹{last_price:.2f} | Predicted Price: ₹{predicted_price:.2f}</div>",
        unsafe_allow_html=True
    )

# =========================
# 💼 PORTFOLIO
# =========================
st.subheader("💼 Portfolio")

col1, col2, col3 = st.columns(3)
p_stock = col1.text_input("Stock Symbol", placeholder="Example: TCS.NS")
p_qty = col2.number_input("Qty", min_value=1, step=1)
p_price = col3.number_input("Buy Price", min_value=1.0, step=1.0)

if st.button("Add"):
    if p_stock.strip():
        st.session_state["portfolio"].append({
            "Stock": p_stock.strip(),
            "Qty": int(p_qty),
            "Buy Price": float(p_price)
        })
    else:
        st.warning("Please enter a stock symbol.")

if st.session_state["portfolio"]:
    pf = pd.DataFrame(st.session_state["portfolio"])
    prices = []

    for s in pf["Stock"]:
        try:
            data = yf.download(s, period="1d", progress=False)
            if not data.empty and "Close" in data.columns:
                prices.append(float(data["Close"].iloc[-1]))
            else:
                prices.append(np.nan)
        except:
            prices.append(np.nan)

    pf["Current"] = prices
    pf["P/L"] = (pf["Current"] - pf["Buy Price"]) * pf["Qty"]
    st.dataframe(pf)

# =========================
# LOGOUT
# =========================
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["start_app"] = False
    st.rerun()

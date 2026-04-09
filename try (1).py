import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as d
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import sqlite3

st.set_page_config(page_title="Stock Sense Analytics", page_icon="📈", layout="wide")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- MATPLOTLIB THEME ----------------
plt.style.use('dark_background')

# ---------------- CSS ----------------
st.markdown("""
<style>
/* Background and Base Styling */
.stApp {
    background: linear-gradient(rgba(10, 14, 23, 0.9), rgba(10, 14, 23, 0.95)),
    url("https://images.unsplash.com/photo-1504384308090-c894fdcc538d");
    background-size: cover;
    background-attachment: fixed;
    color: #E2E8F0;
}

/* Typography */
.title {
    text-align: center;
    background: -webkit-linear-gradient(45deg, #4CAF50, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 55px;
    font-weight: 800;
    margin-bottom: 5px;
}
.subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 20px;
    margin-bottom: 40px;
    font-weight: 300;
}

/* Glassmorphism Cards */
.card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 30px 20px;
    text-align: center;
    color: white;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px 0 rgba(0, 212, 255, 0.2);
    border: 1px solid rgba(0, 212, 255, 0.3);
}
.card-icon {
    font-size: 40px;
    margin-bottom: 15px;
}
.card-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* Info Boxes */
.box {
    background: rgba(255, 255, 255, 0.05);
    border-left: 4px solid #4CAF50;
    padding: 25px;
    border-radius: 12px;
    color: #E2E8F0;
    margin-bottom: 20px;
}
.box h3 {
    margin-top: 0;
    color: white;
}

/* Live Price Display */
.price-display {
    background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(0, 212, 255, 0.1));
    border: 1px solid rgba(0, 212, 255, 0.2);
    padding: 20px 25px;
    border-radius: 16px;
    margin-bottom: 25px;
    border-left: 5px solid #00d4ff;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.price-display h2 {
    font-size: 42px;
    font-weight: 700;
    color: white;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🏠 Home", use_container_width=True):
        # Fix: Route directly to dashboard if logged in
        st.session_state.page = "dashboard" if st.session_state.logged_in else "home"

with c2:
    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.page = "about"

with c3:
    if not st.session_state.logged_in:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.page = "login"
    else:
        st.button("✅ Logged In", disabled=True, use_container_width=True)

with c4:
    if not st.session_state.logged_in:
        if st.button("📝 Signup", use_container_width=True):
            st.session_state.page = "signup"
    else:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "home"
            st.rerun()

st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-top: 5px;'>", unsafe_allow_html=True)

# ---------------- ABOUT PAGE (Accessible anywhere) ----------------
if st.session_state.page == "about":
    st.markdown('<div class="title">ℹ️ About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="box">
        <h3>📊 Stock Sense Analytics</h3>
        <p>A smart, modern platform providing real-time data and AI-powered forecasting for the Indian Stock Market.</p>
        <ul>
            <li><b>Live Market Data:</b> Millisecond accurate LTP pulling via yFinance.</li>
            <li><b>AI Forecast:</b> Advanced ARIMA mathematical modeling for short, mid, and long-term predictions.</li>
            <li><b>Interactive UI:</b> Glassmorphism design system ensuring a fatigue-free analytical experience.</li>
        </ul>
        <br>
        <p><b>🧠 Tech Stack:</b> Python, Streamlit, Pandas, statsmodels, yFinance, Matplotlib<br>
        👨‍💻 Developed by <b>Chaitanya Torankar</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ---------------- UNAUTHENTICATED ROUTES ----------------
if not st.session_state.logged_in:
    
    # HOME
    if st.session_state.page == "home":
        st.markdown('<div class="title">Stock Sense Analytics</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Next-Generation AI Stock Prediction Platform</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.markdown('<div class="card"><div class="card-icon">📊</div><div class="card-title">Analyze Stocks</div>Deep sector insights</div>', unsafe_allow_html=True)
        c2.markdown('<div class="card"><div class="card-icon">🔮</div><div class="card-title">Forecast Prices</div>AI-driven ARIMA models</div>', unsafe_allow_html=True)
        c3.markdown('<div class="card"><div class="card-icon">⚡</div><div class="card-title">Live Data</div>Real-time market updates</div>', unsafe_allow_html=True)

        st.write("<br><br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="box">
                <h3>📍 Why Use This App?</h3>
                <p>✔ Real-time Indian stock market integration</p>
                <p>✔ Sophisticated statistical forecasting (ARIMA)</p>
                <p>✔ Easy-to-read confidence intervals</p>
                <p>✔ Built for both beginners and veterans</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="box" style="border-left-color: #00d4ff;">
                <h3>🔐 Secure Access</h3>
                <p>Navigate to the <b>Login</b> or <b>Signup</b> page to authenticate and unlock the full interactive predictive dashboard.</p>
            </div>
            """, unsafe_allow_html=True)

        st.stop()

    # LOGIN
    elif st.session_state.page == "login":
        st.markdown('<div class="title">Welcome Back</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Securely login to your dashboard</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="box" style="border:none; padding:30px;">', unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login Securely", use_container_width=True, type="primary"):
                c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                result = c.fetchone()

                if result:
                    st.session_state.logged_in = True
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid Credentials ❌")
            st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    # SIGNUP
    elif st.session_state.page == "signup":
        st.markdown('<div class="title">Create Account</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Join the future of stock forecasting</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="box" style="border:none; padding:30px;">', unsafe_allow_html=True)
            new_user = st.text_input("Choose a Username")
            new_pass = st.text_input("Create a Password", type="password")
            
            if st.button("Create Account", use_container_width=True, type="primary"):
                try:
                    c.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_pass))
                    conn.commit()
                    st.success("Account Created Successfully! ✅ You can now login.")
                except: 
                    st.error("Username already exists ❌ Please try another.")
            st.markdown('</div>', unsafe_allow_html=True)
        st.stop()


# =========================
# 📊 DASHBOARD (AFTER LOGIN)
# =========================
if st.session_state.logged_in and st.session_state.page in ["home", "dashboard"]:
    st.markdown('<div class="title" style="text-align:left; font-size:40px;">📊 Intelligence Dashboard</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("### ⚙️ Engine Parameters")

    # Grouping sidebar inputs cleanly
    start_date = st.sidebar.date_input("Training Start Date", d.date(2022, 1, 1))
    end_date = st.sidebar.date_input("Training End Date", d.date.today())

    st.sidebar.markdown("---")
    
    prediction_windows = {"Short term: 7 days": 7, "Mid term: 30 days": 30, "Long term: 90 days": 90}
    selected_window = st.sidebar.selectbox("Prediction Horizon", list(prediction_windows.keys()), index=1)
    forecast_days = prediction_windows[selected_window]

    st.sidebar.markdown("---")

    sector_stocks = {
        "IT": {"TCS": "TCS.NS", "Infosys": "INFY.NS", "Wipro": "WIPRO.NS"},
        "Banking": {"HDFC Bank": "HDFCBANK.NS", "ICICI": "ICICIBANK.NS", "SBI": "SBIN.NS"},
        "FMCG": {"ITC": "ITC.NS", "HUL": "HINDUNILVR.NS", "Nestle": "NESTLEIND.NS"},
        "Energy": {"Reliance": "RELIANCE.NS", "ONGC": "ONGC.NS", "NTPC": "NTPC.NS"},
        "Auto": {"Maruti": "MARUTI.NS", "Tata Motors": "TATAMOTORS.NS", "M&M": "M&M.NS"}
    }

    sector = st.sidebar.selectbox("Market Sector", list(sector_stocks.keys()))
    stock_name = st.sidebar.selectbox("Select Asset", list(sector_stocks[sector].keys()))
    symbol = sector_stocks[sector][stock_name]

    # Quick styling for the logout in sidebar just in case they prefer it there
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout Session", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "home"
        st.rerun()

    ticker = yf.Ticker(symbol)
    
    # 1. Improved Live Price Fetching
    try:
        live_price = ticker.fast_info['last_price']
    except:
        live_data = ticker.history(period="1d")
        live_price = live_data['Close'].iloc[-1] if not live_data.empty else 0.0

    # 2. Historical Data with Frequency Fix
    with st.spinner('Fetching market data and training ARIMA model...'):
        df = ticker.history(start=start_date, end=end_date)

        if len(df) > 10:  # Ensure we have enough data points
            series = df['Close'].resample('B').ffill().dropna()
            
            # --- ROBUST ARIMA LOGIC ---
            try:
                model = ARIMA(series, order=(5, 1, 0), trend='c')
                model_fit = model.fit()
            except ValueError:
                try:
                    model = ARIMA(series, order=(5, 1, 0), trend='t')
                    model_fit = model.fit()
                except:
                    model = ARIMA(series, order=(1, 1, 0), trend='n')
                    model_fit = model.fit()
            except Exception as e:
                st.error(f"Mathematical Error: {e}")
                st.stop()

            # 3. Generate Forecast
            forecast_res = model_fit.get_forecast(steps=forecast_days)
            forecast_values = forecast_res.predicted_mean
            conf_int = forecast_res.conf_int()

            # Align Dates for Charting
            last_date = series.index[-1]
            future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=forecast_days, freq='B')

            # 4. UI Display
            st.markdown(f"""
            <div class="price-display">
                <small style="color:#00d4ff; font-weight:600; letter-spacing: 1px;">{stock_name.upper()} • LIVE MARKET PRICE (LTP)</small>
                <h2>₹{live_price:,.2f}</h2>
                <p style="margin:10px 0 0 0; color:#cbd5e1; font-size: 16px;">
                    <b>Expected Range ({selected_window.split(':')[0]}):</b> 
                    <span style="color:#4CAF50;">₹{conf_int.iloc[:, 0].min():,.2f}</span> 
                    <span style="color:#94A3B8; margin: 0 5px;">&mdash;</span> 
                    <span style="color:#00d4ff;">₹{conf_int.iloc[:, 1].max():,.2f}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Matplotlib Aesthetic Improvements
            fig, ax = plt.subplots(figsize=(12, 5))
            fig.patch.set_alpha(0.0)  # Transparent figure background
            ax.patch.set_alpha(0.0)   # Transparent axis background
            
            # Plotlines
            ax.plot(series.index, series, label="Historical Price", color="#4CAF50", linewidth=1.5)
            ax.plot(future_dates, forecast_values, label="AI Forecast", color="#00d4ff", linestyle="--", linewidth=2)
            ax.fill_between(future_dates, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='#00d4ff', alpha=0.15, label="Confidence Interval")
            
            # Grid and Spines styling
            ax.grid(color='white', alpha=0.05, linestyle='dashed')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # FIXED: Using (R, G, B, Alpha) tuples instead of CSS strings
            ax.spines['left'].set_color((1.0, 1.0, 1.0, 0.2))
            ax.spines['bottom'].set_color((1.0, 1.0, 1.0, 0.2))
            ax.tick_params(colors=(1.0, 1.0, 1.0, 0.6))
            
            ax.set_title(f"{stock_name} ({symbol}) Trajectory Forecast", color="white", pad=20, fontsize=14, fontweight='bold')
            ax.set_ylabel("Price (INR)", color=(1.0, 1.0, 1.0, 0.6))
            
            legend = ax.legend(frameon=False)
            for text in legend.get_texts():
                text.set_color((1.0, 1.0, 1.0, 0.8)) # FIXED

            st.pyplot(fig)

            st.write("<br>", unsafe_allow_html=True)
            with st.expander("📂 View Raw Forecast Data Table"):
                forecast_df = pd.DataFrame({"Predicted Price (INR)": forecast_values.values}, index=future_dates)
                forecast_df.index.name = "Date"
                st.dataframe(forecast_df.style.format("{:.2f}"), use_container_width=True)
                
        else:
            st.warning("⚠️ Not enough historical data found for this date range. Please select an earlier start date.")
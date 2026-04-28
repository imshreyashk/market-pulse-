import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scraper import get_news_headlines
from sentiment_analysis import analyze_sentiment
from financial_engine import get_financial_pulse, get_sector_performance
# Import the new portfolio engine
from portfolio_engine import optimize_portfolio 
import sys
import os
sys.path.append(os.path.dirname(__file__))


# 1. SETUP
st.set_page_config(page_title="MarketPulse Pro", layout="wide", page_icon="🛡️")

# Custom CSS for that "Terminal" look
st.html("""
<style>
    .stMetric { border: 1px solid #333; padding: 15px; border-radius: 10px; background: #161b22; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { border-radius: 5px 5px 0 0; padding: 10px 20px; background: #161b22; }
</style>
""")

st.title("🛡️ MarketPulse: Unified Decision Engine")

# --- GLOBAL MARKET BREADTH ---
with st.expander("🌐 VIEW GLOBAL SECTOR PERFORMANCE", expanded=False):
    if st.button("Refresh Market Data"):
        with st.spinner("Scanning S&P 500 Sectors..."):
            sector_data = get_sector_performance()
            df_sectors = pd.DataFrame(list(sector_data.items()), columns=['Sector', 'Change %'])
            fig = px.treemap(df_sectors, path=['Sector'], values=[1]*len(df_sectors),
                             color='Change %', color_continuous_scale='RdYlGn',
                             color_continuous_midpoint=0)
            st.plotly_chart(fig, use_container_width=True)

# 2. SIDEBAR - Configuration
st.sidebar.header("Configuration")
market_type = st.sidebar.selectbox("Select Market", ["US (NASDAQ/NYSE)", "India (NSE)"])

raw_ticker = st.sidebar.text_input("Enter Ticker (e.g., AAPL or RELIANCE)", "RELIANCE").upper()

if market_type == "India (NSE)":
    if not raw_ticker.endswith(".NS"):
        ticker = f"{raw_ticker}.NS"
    else:
        ticker = raw_ticker
else:
    ticker = raw_ticker.replace(".NS", "")

btn = st.sidebar.button("⚡ GENERATE MASTER PULSE")

# --- NEW SIDEBAR ADDITION: PORTFOLIO OPTIMIZER ---
st.sidebar.divider()
st.sidebar.subheader("🏛️ Portfolio Optimizer")
portfolio_tickers = st.sidebar.multiselect(
    "Select Tickers for Optimization",
    ["AAPL", "TSLA", "NVDA", "RELIANCE.NS", "TCS.NS", "INFY.NS", "GOOGL", "MSFT", "AMZN"],
    default=["AAPL", "RELIANCE.NS", "NVDA"]
)
opt_btn = st.sidebar.button("⚖️ OPTIMIZE WEIGHTS")

# --- PORTFOLIO OPTIMIZATION LOGIC ---
if opt_btn:
    st.header("🏛️ Portfolio Strategy Engine")
    with st.spinner("Calculating Efficient Frontier..."):
        try:
            results = optimize_portfolio(portfolio_tickers)
            
            # Metrics Row
            p_col1, p_col2, p_col3 = st.columns(3)
            p_col1.metric("Expected Annual Return", f"{results['return']:.2f}%")
            p_col2.metric("Annual Volatility (Risk)", f"{results['volatility']:.2f}%")
            p_col3.metric("Sharpe Ratio", f"{results['sharpe']:.2f}")

            # Visualization
            df_weights = pd.DataFrame(list(results['weights'].items()), columns=['Ticker', 'Weight'])
            fig_pie = px.pie(df_weights, values='Weight', names='Ticker', 
                             title="Optimal Capital Allocation",
                             color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.info("💡 **Insight:** This allocation represents the 'Max Sharpe Ratio' portfolio, balancing the highest return possible for every unit of risk taken.")
        except Exception as e:
            st.error(f"Could not optimize portfolio. Error: {e}")

# --- ORIGINAL ANALYSIS LOGIC ---
if btn:
    with st.spinner(f"Analyzing {ticker} Triangle..."):
        headlines = get_news_headlines(ticker)
        fin = get_financial_pulse(ticker)

        if not headlines:
            st.warning(f"No recent news found for {ticker}. Defaulting to neutral sentiment.")
            sentiment = 0.0 
        else:
            sentiment = analyze_sentiment(headlines)

        if fin:
            # 3. VERDICT GAUGE
            master_score = (sentiment * 0.5) + (fin['tech_score'] * 0.3) + (fin['fund_score'] * 0.2)
            
            if master_score > 0.2:
                st.success(f"🚀 **BULLISH CONFIRMATION** | Master Score: {master_score:.2f}")
            elif master_score < -0.2:
                st.error(f"⚠️ **BEARISH WARNING** | Master Score: {master_score:.2f}")
            else:
                st.warning(f"🧊 **NEUTRAL SIGNAL** | Master Score: {master_score:.2f}")

            # --- MARKET MICROSTRUCTURE SUMMARY ---
            with st.container():
                st.markdown("#### 🔍 Market Microstructure Analysis")
                m_col1, m_col2, m_col3 = st.columns(3)
                
                with m_col1:
                    st.write(f"**Fractal Efficiency:** {fin['efficiency']}")
                    st.progress(min(max(fin['efficiency'], 0.0), 1.0))
                
                with m_col2:
                    l_color = "red" if fin['liquidity_risk'] == "High" else "green"
                    st.markdown(f"**Liquidity Risk:** :{l_color}[{fin['liquidity_risk']}]")
                
                with m_col3:
                    st.markdown(f"**Volatility Regime:** `{fin['volatility_regime']}`")
            st.divider()

            # 4. PRO METRIC ROW
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("AI Sentiment", f"{sentiment:.2f}")
            col2.metric("RSI (14d)", f"{fin['rsi']:.1f}", help="Below 30=Oversold, Above 70=Overbought")
            col3.metric("ADX (Trend)", f"{fin['adx']:.1f}", help="Above 25 = Strong Trend")
            col4.metric("Price", f"${fin['current_price']:.2f}", delta=f"{fin['change_pct']:.2f}%")

            # 5. CHARTS & NEWS
            tab1, tab2, tab3 = st.tabs(["📊 Technical Visuals", "📈 Price Analysis", "📰 Evidence Feed"])
            
            with tab1:
                # --- NEW: INTERACTIVE CANDLESTICK CHART ---
                st.subheader("🕯️ Price Action & Trend")
                df = fin['full_history']
                fig_main = go.Figure()
                
                # Candlesticks
                fig_main.add_trace(go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], 
                    low=df['Low'], close=df['Close'], name="Candlesticks"
                ))
                
                # Moving Averages Overlay
                fig_main.add_trace(go.Scatter(x=df.index, y=df['Close'].rolling(50).mean(), 
                                              line=dict(color='orange', width=1.5), name="SMA 50"))
                fig_main.add_trace(go.Scatter(x=df.index, y=df['Close'].rolling(200).mean(), 
                                              line=dict(color='cyan', width=1.5), name="SMA 200"))
                
                fig_main.update_layout(xaxis_rangeslider_visible=False, height=450, 
                                      template="plotly_dark", margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_main, use_container_width=True)
                
                # --- EXISTING METRICS BELOW ---
                if fin['bb_squeeze']:
                    st.warning("🎯 **BOLLINGER SQUEEZE DETECTED**: Volatility is low. A major price breakout is likely imminent.")

                c1, c2, c3 = st.columns(3)
                with c1:
                    fig_rsi = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = fin['rsi'],
                        title = {'text': "RSI (Momentum)"},
                        gauge = {
                            'axis': {'range': [0, 100]},
                            'steps': [
                                {'range': [0, 30], 'color': "#238636"},
                                {'range': [70, 100], 'color': "#da3633"}]}))
                    st.plotly_chart(fig_rsi, use_container_width=True)
                
                with c2:
                    fig_cmf = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = fin['cmf'],
                        title = {'text': "Money Flow (CMF)"},
                        gauge = {
                            'axis': {'range': [-1, 1]},
                            'bar': {'color': "#58a6ff"},
                            'steps': [
                                {'range': [-1, -0.05], 'color': "#da3633"},
                                {'range': [0.05, 1], 'color': "#238636"}]}))
                    st.plotly_chart(fig_cmf, use_container_width=True)

                with c3:
                    fig_adx = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = fin['adx'],
                        title = {'text': "Trend Strength (ADX)"},
                        gauge = {
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "gold"},
                            'steps': [
                                {'range': [0, 25], 'color': "gray"},
                                {'range': [25, 100], 'color': "#238636"}]}))
                    st.plotly_chart(fig_adx, use_container_width=True)

            with tab2:
                st.subheader("Price vs Key Averages (Trend Support)")
                bench_data = pd.DataFrame({
                    "Levels": [fin['sma_200'], fin['sma_50'], fin['current_price']]
                }, index=["SMA 200 (Long Term)", "SMA 50 (Mid Term)", "Current Price"])
                st.bar_chart(bench_data)
                
                if fin['current_price'] > fin['sma_50']:
                    st.info(f"💡 Price is trading ABOVE the 50-day average. The short-term trend is **Strong**.")

            with tab3:
                st.subheader("Headlines Analyzed by AI")
                news_df = pd.DataFrame(headlines, columns=["Headline"])
                st.dataframe(news_df, use_container_width=True, height=400)
        else:
            st.error("Ticker not found. Please check the symbol.")

st.divider()
st.caption("🛡️ MarketPulse Pro | Unified Intelligence Terminal")
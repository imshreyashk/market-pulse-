import yfinance as yf
import pandas as pd
import numpy as np

SECTORS = {
    "Technology": "XLK", "Financials": "XLF", "Healthcare": "XLV",
    "Energy": "XLE", "Consumer Disc": "XLY", "Industrials": "XLI",
    "Utilities": "XLU", "Materials": "XLB", "Real Estate": "XLRE",
    "Communication": "XLC", "Consumer Staples": "XLP",
    "Nifty Bank": "^NSEBANK",
    "Nifty IT": "^CNXIT",
    "Nifty Pharma": "^CNXPHARMA",
    "Nifty Metal": "^CNXMETAL",
    "Nifty FMCG": "^CNXFMCG",
    "Nifty Auto": "^CNXAUTO",
    "Nifty Realty": "^CNXREALTY",
    "Nifty Energy": "^CNXENERGY",
    "Nifty Media": "^CNXMEDIA"
}

def get_sector_performance():
    performance = {}
    for name, ticker in SECTORS.items():
        data = yf.Ticker(ticker).history(period="5d")
        # Calculate percentage change for the last trading day
        change = ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
        performance[name] = round(change, 2)
    return performance

# --- NEW MICROSTRUCTURE FUNCTION ---
def get_microstructure_analysis(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    # Get high-frequency intraday data (5 days of 5-minute bars)
    intraday = stock.history(period="5d", interval="5m")
    
    if intraday.empty:
        return {"efficiency": 0, "liquidity_risk": "N/A", "volatility_regime": "N/A"}

    # 1. Efficiency Ratio (Fractal Efficiency)
    net_change = abs(intraday['Close'].iloc[-1] - intraday['Close'].iloc[0])
    individual_changes = intraday['Close'].diff().abs().sum()
    efficiency = (net_change / individual_changes) if individual_changes != 0 else 0

    # 2. Relative Spread Proxy
    avg_spread = ((intraday['High'] - intraday['Low']) / intraday['Close']).mean()
    
    # 3. Volatility Regime
    return {
        "efficiency": round(efficiency, 2), 
        "liquidity_risk": "High" if avg_spread > 0.005 else "Low",
        "volatility_regime": "Trending" if efficiency > 0.15 else "Ranging/Noisy"
    }

def get_financial_pulse(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    # 1. Technical Analysis (1-Year History)
    hist = stock.history(period="1y")
    if hist.empty:
        return None
    
    # Calculate 50-day and 200-day Moving Averages
    sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
    sma_200 = hist['Close'].rolling(window=200).mean().iloc[-1]
    current_price = hist['Close'].iloc[-1]

    # RSI CALCULATION (14-period) ---
    delta = hist['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs)).iloc[-1]

    avg_volume = hist['Volume'].tail(20).mean()
    current_volume = hist['Volume'].iloc[-1]
    vol_ratio = current_volume / avg_volume

    # --- NEW INDICATORS LOGIC START ---
    
    # 1. Bollinger Bands (Squeeze)
    sma_20 = hist['Close'].rolling(window=20).mean()
    std_20 = hist['Close'].rolling(window=20).std()
    upper_bb = sma_20 + (std_20 * 2)
    lower_bb = sma_20 - (std_20 * 2)
    bb_width = (upper_bb.iloc[-1] - lower_bb.iloc[-1]) / sma_20.iloc[-1]
    bb_squeeze = bb_width < 0.1  # True if volatility is coiling

    # 2. Chaikin Money Flow (CMF)
    mf_multiplier = ((hist['Close'] - hist['Low']) - (hist['High'] - hist['Close'])) / (hist['High'] - hist['Low'])
    mf_multiplier = mf_multiplier.fillna(0)
    mf_volume = mf_multiplier * hist['Volume']
    cmf = mf_volume.rolling(20).sum() / hist['Volume'].rolling(20).sum()
    current_cmf = cmf.iloc[-1]

    # 3. ADX (Trend Strength - 14 period)
    plus_dm = hist['High'].diff()
    minus_dm = hist['Low'].diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr = pd.concat([hist['High'] - hist['Low'], 
                    (hist['High'] - hist['Close'].shift()).abs(), 
                    (hist['Low'] - hist['Close'].shift()).abs()], axis=1).max(axis=1)
    
    atr = tr.rolling(window=14).mean()
    plus_di = 100 * (plus_dm.rolling(window=14).mean() / atr)
    minus_di = 100 * (minus_dm.abs().rolling(window=14).mean() / atr)
    dx = (100 * (plus_di - minus_di).abs() / (plus_di + minus_di)).rolling(window=14).mean()
    current_adx = dx.iloc[-1]

    # --- NEW INDICATORS LOGIC END ---

    # Call Microstructure for returning detailed data
    micro = get_microstructure_analysis(ticker_symbol)
    
    # Technical Score Logic (-1 to 1)
    tech_score = 0
    if current_price > sma_50 > sma_200: tech_score += 0.5  # Bullish trend
    if current_price < sma_50 < sma_200: tech_score -= 0.5  # Bearish trend
    if rsi < 30: tech_score += 0.4  # Oversold
    if rsi > 70: tech_score -= 0.4  # Overbought
    if vol_ratio > 1.5: tech_score *= 1.2 

    # 2. Fundamental Analysis (P/E Ratio)
    info = stock.info
    pe_ratio = info.get('trailingPE', 25) 
    fund_score = 0
    if pe_ratio < 20: fund_score = 0.3  
    elif pe_ratio > 40: fund_score = -0.3 
    
    return {
        "current_price": current_price,
        "sma_50": sma_50,
        "rsi": rsi,
        "vol_ratio": vol_ratio,
        "sma_200": sma_200,
        "pe_ratio": pe_ratio,
        "tech_score": tech_score,
        "fund_score": fund_score,
        "change_pct": ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100,
        "bb_squeeze": bb_squeeze,
        "cmf": current_cmf,
        "adx": current_adx,
        "efficiency": micro['efficiency'],
        "liquidity_risk": micro['liquidity_risk'],
        "volatility_regime": micro['volatility_regime'],
        # ADD THIS LINE:
        "full_history": hist 
    }
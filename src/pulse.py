import yfinance as yf  # Library to get stock market data from Yahoo Finance
import pandas as pd    # Library for data manipulation (tables/dataframes)

def get_market_data(ticker="NVDA"):
    """
    Step 1: Get the Price.
    We are downloading 'Nvidia' stock data.
    period='1d': We only want today's data.
    interval='15m': We want a price update every 15 minutes.
    """
    print(f"📈 Fetching live data for {ticker}...")
    
    # yf.download is a function that talks to Yahoo's servers
    data = yf.download(ticker, period="1d", interval="15m")
    
    # data.tail() shows the last 5 rows of the table (the most recent prices)
    print(data.tail())
    return data

if __name__ == "__main__":
    # This part only runs if you run this specific file.
    get_market_data()
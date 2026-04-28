import yfinance as yf
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

def optimize_portfolio(tickers):
    # 1. Download data for all tickers
    data = yf.download(tickers, period="2y")['Close']
    
    # 2. Calculate Expected Returns and Sample Covariance
    mu = expected_returns.mean_historical_return(data)
    S = risk_models.sample_cov(data)

    # 3. Optimize for Maximal Sharpe Ratio (Best Risk/Return balance)
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    
    # 4. Get Performance Metrics
    ret, vol, sharpe = ef.portfolio_performance(verbose=False)
    
    return {
        "weights": cleaned_weights,
        "return": ret * 100,
        "volatility": vol * 100,
        "sharpe": sharpe
    }
# 🛡️ MarketPulse Pro: AI-Driven Financial Decision Engine

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![MLflow](https://img.shields.io/badge/MLOps-MLflow-orange.svg)](https://mlflow.org/)

**MarketPulse Pro** is an end-to-end Machine Learning system that automates stock market "Mood" tracking. It moves beyond simple price charts by using **FinBERT** (Financial BERT) to analyze global news sentiment and cross-reference it with technical momentum.

---

## 🎯 The Problem
Individual traders often suffer from **"Information Overload"** and **"Emotional Bias."** MarketPulse solves this by quantifying the news cycle into a mathematical "Master Pulse" score.

## 🛠️ The Triangle of Truth (System Architecture)

The engine calculates a **Master Confidence Score** based on three distinct legs:
1.  **Sentiment Leg (AI):** Real-time web scraping of headlines processed through the **Hugging Face FinBERT** model.
2.  **Technical Leg (Math):** Analysis of 50-day vs. 200-day Moving Averages via `yfinance`.
3.  **Fundamental Leg (Health):** Valuation tracking (P/E Ratios) to avoid overvalued traps.



---

## 🚀 Features
* **Live Dashboard:** Built with Streamlit for real-time ticker analysis.
* **Multi-Stock Watchlist:** Compare high-growth tickers (e.g., NVDA, TSLA) on a single leaderboard.
* **Telegram Sentry Bot:** Asynchronous background monitoring that pushes alerts to your phone when "Buy Signals" are detected.
* **MLOps Tracking:** All model inferences are logged in MLflow for performance auditing.
* **CI/CD Pipeline:** Automated testing and Docker builds via GitHub Actions.

## 🐳 Getting Started (Docker)
Ensure you have Docker installed, then run:
```bash
docker-compose up --build
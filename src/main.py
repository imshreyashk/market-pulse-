import mlflow
from scraper import get_news_headlines
from sentiment_analysis import analyze_sentiment
import os
# 1. SET THE EXPERIMENT: This creates a folder to store all your MarketPulse runs
mlflow.set_experiment("Market_Sentiment_Pulse")

# This tells MLflow: "Store everything in the root mlruns folder no matter where I run from"
mlruns_dir = os.path.join(os.getcwd(), "mlruns")
mlflow.set_tracking_uri(f"file:///{mlruns_dir}")

def run_mlops_pipeline(ticker):
    # 2. START THE RUN: This is the "Diary" entry for this specific check
    with mlflow.start_run(run_name=f"Pulse_{ticker}"):
        
        print(f"📡 Tracking Sentiment for: {ticker}")
        
        # --- PHASE: SCRAPING ---
        headlines = get_news_headlines(ticker)
        
        # LOG PARAMS: We record what ticker we searched for
        mlflow.log_param("ticker", ticker)
        mlflow.log_param("headline_count", len(headlines))
        
        # --- PHASE: SENTIMENT ---
        pulse_score = analyze_sentiment(headlines)
        
        # LOG METRICS: We record the numerical result
        mlflow.log_metric("sentiment_score", pulse_score)
        
        # LOG ARTIFACTS: We save the raw headlines so we know WHY the score was high/low
        with open("latest_headlines.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(headlines))
        mlflow.log_artifact("latest_headlines.txt")

        # --- PHASE: VERDICT ---
        print(f"📊 Score for {ticker}: {pulse_score:.4f}")
        mlflow.set_tag("market_status", "Bullish" if pulse_score > 0.1 else "Bearish")

if __name__ == "__main__":
    ticker = input("Ticker to track: ").upper()
    run_mlops_pipeline(ticker)
    print("✅ Run logged to MLflow. Type 'mlflow ui' to see it!")
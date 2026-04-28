from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

#!. The model loading: we load the finbert brain.
#FinBERT is special because it knows that the word 'Down' is BAD in finance
#but might be NEUTRAL in regular movie review.

model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def analyze_sentiment(headlines):
    """
    Logic: Converts a list of text into a single sentiment pulse (-1.0 to 1.0)
    """

    if not headlines or len(headlines) == 0:
        return 0.0  # Neutral if no news
#2. TOKENIZATION: Transformers can't read 'Nvidia'.
#This turns words into 'Tensors' (multidimensional arrays of numbers).
    inputs = tokenizer(headlines, padding=True, truncation=True, return_tensors='pt')

#3. INFERENCE: We pass the numbers through the neural network.
#torch.no_grad() saves memory beacause we aren't training(learning)
    with torch.no_grad():
        outputs = model(**inputs)

#4. SENTIMENT SCORES: The model gives us 'logits' (raw scores).
#Softmax turn them into probabilities (e.g., 90% positive, 5% Negative, 5% Neutral).
#FinBERT labels are ordered as [0: Positive, 1: Negative, 2: Neutral]
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

#5. Calculation: To get a single 'pulse' score:
#We subtract the 'Negative' probability from the 'Positive' probability.
#Result: +1.0 is pure hype, -1.0 is pure panic, 0.0 is neutral.
    sentiment_scores = probabilities[:, 0] - probabilities[:, 1]

#we average the score of all 10 headlines.
    avg_score = torch.mean(sentiment_scores).item()
    return avg_score

if __name__ =="__main__":
    #Test the brain
    sample_news = [
        "Nvidia quarterly earnings crush expectations",
        "Market analysts warn of potential tech bubble"
    ]

    pulse = analyze_sentiment(sample_news)
    print(f"📊 Sentiment Pulse: {pulse:.2f}")

    if pulse > 0.2: print("🚀 Positive Sentiment Detected!")
    elif pulse < -0.2: print("⚠️ Negative Sentiment Detected!")
    else: print("😐 Neutral Sentiment Detected. (Wait) 🧊")
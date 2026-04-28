from matplotlib import ticker
import requests
from bs4 import BeautifulSoup

def get_news_headlines(ticker="NVDA"):
    # 1. THE TARGET: We use the ticker symbol to build the URL.
    # Finviz is structured so that adding '?t=TICKER' takes you straight to the data.
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    
    # 2. THE DISGUISE (Headers): Most sites block simple scripts to prevent spam.
    # By adding a 'User-Agent', we tell the server: "I am a human on a Chrome browser."
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 3. THE REQUEST: Visit the URL and get the HTML code.
    response = requests.get(url, headers=headers)
    
    # 4. THE SOUP: BeautifulSoup 'parses' the messy HTML code into a clean tree structure.
    soup = BeautifulSoup(response.content, 'html.parser')

    #5. THE EXTRACTION: Finviz keeps all news in <table> with ID 'news-table'.
    news_table = soup.find(id='news-table')

    # 6. THE HEADLINES: Each news item is in a <tr> (table row).
    headlines = []
    if news_table:
        for row in news_table.findAll('tr'):
            headline = row.a.get_text()  # Get the text of the link (the headline)
            headlines.append(headline)

    return headlines[:10]

if __name__ == "__main__":
    # Test the scraper
    print(f"🔎 Scraping news for NVDA...")
    headlines = get_news_headlines("NVDA")
    for i, h in enumerate(headlines, 1):
        print(f"{i}. {h}")

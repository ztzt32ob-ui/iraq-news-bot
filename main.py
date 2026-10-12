
import os
import time
import feedparser
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHANNEL = "@iraqnews964"

FEEDS = [
    "https://feeds.bbci.co.uk/arabic/middleeast/rss.xml",
    "https://www.aljazeera.net/aljazeerarss/arabic/news.xml",
]

def send_news(title, link):
    text = f"📰 {title}\n\n🔗 {link}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(
        url,
        data={"chat_id": CHANNEL, "text": text},
        timeout=20,
    )
    response.raise_for_status()

seen = set()

while True:
    for feed_url in FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in reversed(feed.entries[:10]):
                link = entry.get("link", "")
                title = entry.get("title", "")
                if link and title and link not in seen:
                    send_news(title, link)
                    seen.add(link)
                    time.sleep(2)
        except Exception as error:
            print("News error:", error)

    time.sleep(900)
  

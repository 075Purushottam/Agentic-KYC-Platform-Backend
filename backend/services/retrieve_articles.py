from dataclasses import dataclass
import json

@dataclass
class MediaArticle:
    title: str
    description: str
    source: str
    url: str
    published_at: str
    content: str
    provider: str

def normalize_newsapi(data):
    articles = []

    for item in data.get("articles", []):
        articles.append(
            MediaArticle(
                title=item.get("title", ""),
                description=item.get("description", ""),
                source=item.get("source", {}).get("name", ""),
                url=item.get("url", ""),
                published_at=item.get("publishedAt", ""),
                content=item.get("content", ""),
                provider="NEWS_API"
            )
        )

    return articles

def normalize_gnews(data):
    articles = []

    for item in data:
        articles.append(
            MediaArticle(
                title=item.get("title", ""),
                description=item.get("description", ""),
                source=item.get("source", {}).get("name", ""),
                url=item.get("url", ""),
                published_at=item.get("publishedAt", ""),
                content=item.get("content", ""),
                provider="GNEWS"
            )
        )

    return articles

from bs4 import BeautifulSoup

def normalize_feedparser(feed):
    articles = []

    for entry in feed.entries:

        summary = BeautifulSoup(
            entry.get("summary", ""),
            "html.parser"
        ).get_text()

        articles.append(
            MediaArticle(
                title=entry.get("title", ""),
                description=summary,
                source=entry.get("source", {}).get("title", ""),
                url=entry.get("link", ""),
                published_at=entry.get("published", ""),
                content=summary,
                provider="RSS"
            )
        )

    return articles

results = []
def feedparser_end(q):
    import feedparser
    import json
    import urllib.parse

    queries = [q]
    feeds = []
    for q in queries:
        q = urllib.parse.quote(q)
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en")
        res = normalize_feedparser(feed)
        results.extend(res)

def gnews_end(q):
    import json
    import urllib.request

    apikey = "41a3b83e2d94860a6efa5beaf56cc30a"
    url = f"https://gnews.io/api/v4/search?q=vaibhav%20suryavanshi&country=IN&lang=en&max=10&apikey={apikey}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        
        normalized_articles = normalize_gnews(data.get("articles", []))
        results.extend(normalized_articles)

def newsapi_end(q):
    import requests
    url = "https://newsapi.org/v2/everything"
    apikey = "abaaade4a0ed48c0b24789f47dfb7c78"
    querystring = {"q":q + "rajesh exports scam","apiKey":apikey}
    response = requests.request("GET", url, params=querystring)
    normalized_articles = normalize_newsapi(response.json())
    results.extend(normalized_articles)

def extract_articles(customer_details):
    name=customer_details['name']
    country=customer_details['country']
    # newsapi_end(name + country)
    feedparser_end(name+ " " + country + " " + "scam")
    return results





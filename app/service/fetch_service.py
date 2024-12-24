import time
from geopy.geocoders import Nominatim
import groq
import json
from app.db.elastic_setting.config import Config
from typing import List, Dict, Any, Optional
import requests
from functools import lru_cache
from app.db.models.elastic_models import Coordinates, NewsClassification, NewsCategory
from app.service.elastic_service import save_to_elasticsearch_for_news

groq_client = groq.Client(api_key=Config.GROQ_API_KEY)
geolocator = Nominatim(user_agent="terror_analysis")


def fetch_news() -> List[Dict[str, Any]]:
    url = "https://eventregistry.org/api/v1/article/getArticles"

    body = {
        "action": "getArticles",
        "keyword": "terror attack",
        "articlesPage": 1,
        "articlesCount": 1,
        "articlesSortBy": "socialScore",
        "articlesSortByAsc": False,
        "dataType": ["news"],
        "apiKey": Config.NEWS_API_KEY
    }

    try:
        response = requests.post(url, json=body)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text[:500]}")

        response.raise_for_status()

        data = response.json()
        return data.get('articles', {}).get('results', [])

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

@lru_cache(maxsize=1000)
def get_coordinates(location: str) -> Optional[Coordinates]:
    try:
        result = geolocator.geocode(location)
        if result:
            return Coordinates(
                latitude=result.latitude,
                longitude=result.longitude
            )
        return None
    except Exception as e:
        print(f"Error getting coordinates for {location}: {e}")
        return None


def classify_news(title: str, content: str) -> Optional[NewsClassification]:
    clean_title = title.replace('\\', '')
    clean_content = content.replace('\\', '') if content else ''

    prompt = f"""
    Classify this news article into one category:
    Choose exactly one of: terror_event, historic_terror, general_news

    Title: {clean_title}
    Content: {clean_content}

    Respond in this exact JSON format:
    {{
        "category": "terror_event",
        "location": "city, country",
        "confidence": 0.9
    }}
    """

    try:
        completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",
            temperature=0.1,
            max_tokens=200
        )

        result = json.loads(completion.choices[0].message.content.strip())

        if result["category"] not in [cat.value for cat in NewsCategory]:
            print(f"Invalid category received: {result['category']}")
            result["category"] = "general_news"

        coords = get_coordinates(result["location"])

        return NewsClassification(
            category=NewsCategory(result["category"]),
            location=result["location"],
            confidence=float(result["confidence"]),
            coordinates=coords
        )

    except Exception as e:
        print(f"Classification error: {str(e)}")
        return None


def process_news():
    articles = fetch_news()
    for article in articles:
        try:
            if not article.get("title") or not article.get("body"):
                continue

            classification = classify_news(
                article.get("title", ""),
                article.get("body", "")
            )

            if classification:
                try:
                    save_to_elasticsearch_for_news(article, classification)
                    print(f"Saved article: {article.get('title')[:50]}...")
                except Exception as e:
                    print(f"Error saving to elasticsearch: {e}")

        except Exception as e:
            print(f"Error processing article: {e}")
            continue


def process_news_every_2_min():
    while True:
        process_news()
        time.sleep(120)
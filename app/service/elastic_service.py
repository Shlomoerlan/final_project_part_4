from typing import List, Dict, Any
from app.db.elastic_setting.config import Config
from app.db.elastic_setting.elastic_connect import elastic_client
from app.db.models import TerrorEvent, NewsClassification


def save_to_elasticsearch_for_news(article: Dict[str, Any], classification: NewsClassification):
    print("Saving article:", article)
    print("Classification:", classification)

    doc = {
        "title": article.get("title"),
        "content": article.get("body"),
        "publication_date": article.get("dateTime"),
        "category": classification.category.value,
        "location": classification.location,
        "confidence": classification.confidence,
        "source_url": article.get("url"),
    }

    if classification.coordinates:
        doc["coordinates"] = {
            "lat": classification.coordinates.latitude,
            "lon": classification.coordinates.longitude
        }
    try:
        elastic_client.index(index=Config.ES_INDEX_FOR_NEWS, document=doc)
        print(f"Successfully saved article: {article.get('title')[:50]}...")
    except Exception as e:
        print(f"Error in save_to_elasticsearch: {str(e)}")
        print(f"Document attempted to save: {doc}")


def save_events_for_terror(events: List[TerrorEvent]) -> None:
    for event in events:
        try:
            elastic_client.index(
                index=Config.ES_INDEX_FOR_TERROR,
                document=event.to_elastic_doc()
            )
        except Exception as e:
            print(f"Error saving event: {e}")
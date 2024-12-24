from typing import List, Dict, Any, Optional
from elasticsearch import Elasticsearch
from app.db.models import SearchParams

def build_elasticsearch_query(params: SearchParams) -> Dict[str, Any]:
    query = {
        "bool": {
            "should": [
                {"match": {"title": {"query": params.query, "boost": 2.0}}},
                {"match": {"content": params.query}},
                {"match": {"location": params.query}}
            ],
            "minimum_should_match": 1
        }
    }

    if params.start_date or params.end_date:
        date_range = {}
        if params.start_date:
            date_range["gte"] = params.start_date.isoformat()
        if params.end_date:
            date_range["lte"] = params.end_date.isoformat()
        query["bool"]["must"] = [{"range": {"publication_date": date_range}}]

    return {
        "size": params.limit,
        "query": query,
        "_source": ["title", "content", "publication_date", "category", "location", "coordinates"],
        "sort": [{"_score": "desc"}]
    }


def get_indices_for_search(source: Optional[str]) -> List[str]:
    if not source:
        return ["news_events", "terror_data"]
    elif source == "news":
        return ["news_events"]
    return ["terror_data"]


def execute_search(
    elastic_client: Elasticsearch,
    params: SearchParams
    ) -> List[Dict[str, Any]]:

    query = build_elasticsearch_query(params)
    indices = get_indices_for_search(params.source)

    print(f"Searching with query: {query}")
    print(f"In indices: {indices}")
    results = elastic_client.search(
        index=indices,
        body=query
    )
    hits = results['hits']['hits']
    print(f"Found {len(hits)} results")  # debug log
    return [hit["_source"] for hit in hits]
from flask import Blueprint, request, render_template
from datetime import datetime
from app.db.elastic_setting.elastic_connect import elastic_client
from app.db.models import SearchParams
from app.service.search_service import execute_search
from app.service.map_service import create_map_from_results

search_routes = Blueprint('search', __name__, url_prefix='/search')


@search_routes.route('/')
def search_page():
    return render_template('search.html')


@search_routes.route("/keywords")
def keywords():
    query = request.args.get('query', '')
    limit = int(request.args.get('limit', 100))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    params = SearchParams(
        query=query,
        limit=limit,
        start_date=datetime.fromisoformat(start_date) if start_date else None,
        end_date=datetime.fromisoformat(end_date) if end_date else None
    )
    results = execute_search(elastic_client, params)
    return create_map_from_results(results)


@search_routes.route("/news")
def news():
    query = request.args.get('query', '')
    limit = int(request.args.get('limit', 100))

    params = SearchParams(query=query, limit=limit, source="news")
    results = execute_search(elastic_client, params)
    return create_map_from_results(results)


@search_routes.route("/historic")
def historic():
    query = request.args.get('query', '')
    limit = int(request.args.get('limit', 100))

    params = SearchParams(query=query, limit=limit, source="historic")
    results = execute_search(elastic_client, params)
    return create_map_from_results(results)


@search_routes.route("/combined")
def combined():
    query = request.args.get('query', '')
    limit = int(request.args.get('limit', 100))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None

    params = SearchParams(
        query=query,
        start_date=start,
        end_date=end,
        limit=limit
    )
    results = execute_search(elastic_client, params)
    return create_map_from_results(results)


@search_routes.get("/search/keywords")
def search_keywords(query: str, limit: int = 100):
    params = SearchParams(query=query, limit=limit)
    results = execute_search(elastic_client, params)
    return create_map_from_results(results)


# backend/api/search.py
from flask import Blueprint, request, jsonify, current_app
from adapters.dev_mock import DevMockAdapter

bp = Blueprint("search", __name__)

# adapter registry (simple)
ADAPTERS = {
    "mock": DevMockAdapter()
}

@bp.route("/", methods=["GET", "POST"])
def search():
    try:
        data = request.get_json() if request.method == "POST" else request.args
        
        query = data.get("query", "")
        max_results = data.get("max_results", 10)
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Use mock adapter
        adapter = ADAPTERS["mock"]
        results = adapter.search(query, max_results)
        
        return jsonify({"results": results, "best": results[:3]}), 200
        
    except Exception as e:
        current_app.logger.error(f"Search error: {str(e)}")
        return jsonify({"error": "Search failed"}), 500

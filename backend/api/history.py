# backend/api/history.py
from flask import Blueprint, request, jsonify
from core.db import get_db

bp = Blueprint("history", __name__)

@bp.route("/product", methods=["GET"])
def product_history():
    product_id = request.args.get("product_id")
    if not product_id:
        return jsonify({"error": "product_id required"}), 400
    db = get_db()
    hist = db.price_history.find_one({"product_id": product_id})
    if not hist:
        return jsonify({"history": []}), 200
    return jsonify(hist.get("history", [])), 200

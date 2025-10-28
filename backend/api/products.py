# backend/api/products.py
from flask import Blueprint, request, jsonify
from core.db import get_db
from bson.objectid import ObjectId

bp = Blueprint("products", __name__)

# -------------------- Existing Routes --------------------
@bp.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    db = get_db()
    p = db.products.find_one({"_id": ObjectId(product_id)})
    if not p:
        return jsonify({"error": "Not found"}), 404
    p["id"] = str(p["_id"])
    p.pop("_id", None)
    return jsonify(p), 200


@bp.route("/", methods=["GET"])
def list_products():
    db = get_db()
    items = []
    for p in db.products.find().limit(100):
        p["id"] = str(p["_id"])
        p.pop("_id", None)
        items.append(p)
    return jsonify(items), 200

# -------------------- New Routes --------------------
@bp.route("/", methods=["POST"])
def add_product():
    """Add a new product to track"""
    data = request.json
    required = ("name", "url", "target_price")
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    product = {
        "name": data["name"],
        "url": data["url"],
        "target_price": float(data["target_price"]),
        "current_price": None,
    }
    result = db.products.insert_one(product)
    return jsonify({"message": "Product added", "id": str(result.inserted_id)}), 201


@bp.route("/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a tracked product"""
    db = get_db()
    result = db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"message": "Product deleted"}), 200

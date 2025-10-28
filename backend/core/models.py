from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from flask import current_app

def get_collection():
    client = MongoClient(current_app.config["MONGO_URI"])
    db = client.get_default_database()
    return db["products"]

def add_product(data):
    product = {
        "name": data["name"],
        "url": data["url"],
        "target_price": float(data["target_price"]),
        "current_price": None,
        "created_at": datetime.utcnow()
    }
    return get_collection().insert_one(product).inserted_id

def get_products():
    products = list(get_collection().find())
    for p in products:
        p["_id"] = str(p["_id"])
    return products

def delete_product(product_id):
    return get_collection().delete_one({"_id": ObjectId(product_id)})

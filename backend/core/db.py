# backend/core/db.py
from pymongo import MongoClient
from flask import current_app, g

def init_db(app):
    mongo_uri = app.config.get("MONGO_URI")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    # Simple connectivity test
    client.admin.command('ping')
    db = client.get_default_database()
    app.mongo_client = client
    app.db = db

def get_db():
    # This returns the DB instance (use inside request handlers)
    from flask import current_app
    return current_app.db

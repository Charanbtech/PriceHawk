# backend/config.py
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/pricehawk")
JWT_SECRET = os.getenv("JWT_SECRET", "jwt_secret")
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")

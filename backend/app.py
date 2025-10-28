import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from core.db import init_db
from core.utils import setup_logging
from api import create_api_blueprint
from jobs.scheduler import init_scheduler


def create_app(config_object=None):
    """Factory function to create and configure the Flask app."""
    # Load environment variables from .env (important for Docker Compose)
    load_dotenv()

    app = Flask(__name__, instance_relative_config=False)

    # Core configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev_secret"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET", "jwt_secret"),
        JWT_ACCESS_TOKEN_EXPIRES=False,  # Tokens don't expire
        MONGO_URI=os.getenv("MONGO_URI", "mongodb://localhost:27017/pricehawk"),
        ENV=os.getenv("FLASK_ENV", "production"),
        # Email configuration
        SENDER_EMAIL=os.getenv("SENDER_EMAIL"),
        SENDER_EMAIL_PASSWORD=os.getenv("SENDER_EMAIL_PASSWORD"),
    )

    # Enable CORS (for frontend communication)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize JWT Manager
    jwt = JWTManager(app)

    # Setup structured logging
    logger = setup_logging(app)
    logger.info("🚀 Starting PriceHawk backend initialization...")

    # Database Initialization
    try:
        init_db(app)
        logger.info("✅ MongoDB connection established successfully.")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")

    # Register API Blueprints
    try:
        api_bp = create_api_blueprint()
        app.register_blueprint(api_bp, url_prefix="/api")
        logger.info("✅ API Blueprints registered successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to register blueprints: {e}")

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "message": "PriceHawk backend is healthy",
            "environment": app.config["ENV"]
        }), 200

    # Scheduler Initialization
    try:
        init_scheduler(app)
        logger.info("✅ Background scheduler initialized.")
    except Exception as e:
        logger.error(f"❌ Failed to start scheduler: {e}")

    logger.info("🎯 PriceHawk backend initialized successfully.")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)

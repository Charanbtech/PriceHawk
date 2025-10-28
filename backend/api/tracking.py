# backend/api/tracking.py
import logging
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId

from core.schemas import TrackProductRequest, UpdateTrackingRequest
from services.tracking import TrackingService

logger = logging.getLogger(__name__)
bp = Blueprint("tracking", __name__)

# Initialize services
tracking_service = TrackingService()

@bp.route("/products", methods=["GET"])
@jwt_required()
def get_tracked_products():
    """Get all products tracked by the current user."""
    user_id = get_jwt_identity()
    
    try:
        tracked_products = tracking_service.get_tracked_products(user_id)
        return jsonify({
            "status": "success",
            "count": len(tracked_products),
            "products": tracked_products
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving tracked products: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve tracked products"
        }), 500

@bp.route("/track", methods=["POST"])
@jwt_required()
def track_product():
    """Start tracking a product for the current user."""
    user_id = get_jwt_identity()
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        # Validate request data
        track_request = TrackProductRequest(**data)
        
        # Track the product
        result = tracking_service.track_product(user_id, track_request.dict())
        
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Error tracking product: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to track product"
        }), 500

@bp.route("/untrack/<product_id>", methods=["DELETE"])
@jwt_required()
def untrack_product(product_id):
    """Stop tracking a product for the current user."""
    user_id = get_jwt_identity()
    
    try:
        result = tracking_service.untrack_product(user_id, product_id)
        
        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        logger.error(f"Error untracking product: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to untrack product"
        }), 500

@bp.route("/preferences/<product_id>", methods=["PATCH"])
@jwt_required()
def update_tracking_preferences(product_id):
    """Update tracking preferences for a product."""
    user_id = get_jwt_identity()
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        # Validate request data
        update_request = UpdateTrackingRequest(**data)
        
        # Update tracking preferences
        result = tracking_service.update_tracking_preferences(
            user_id, 
            product_id, 
            update_request.dict(exclude_unset=True)
        )
        
        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating tracking preferences: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to update tracking preferences"
        }), 500

@bp.route("/history/<product_id>", methods=["GET"])
@jwt_required()
def get_price_history(product_id):
    """Get price history for a product."""
    try:
        days = request.args.get("days", default=None, type=int)
        
        price_history = tracking_service.get_price_history(product_id, days)
        
        return jsonify({
            "status": "success",
            "product_id": product_id,
            "price_history": price_history
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving price history: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve price history"
        }), 500

@bp.route("/forecast/<product_id>", methods=["GET"])
@jwt_required()
def forecast_product_price(product_id):
    """Get price forecast for a product."""
    try:
        days_ahead = request.args.get("days", default=7, type=int)
        # Lazy import to avoid heavy dependencies at startup
        from services.forecasting import ForecastingService
        forecasting_service = ForecastingService()

        forecast = forecasting_service.forecast_price(product_id, days_ahead)
        
        return jsonify(forecast), 200
    except Exception as e:
        logger.error(f"Error generating price forecast: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to generate price forecast"
        }), 500

@bp.route("/analysis/<product_id>", methods=["GET"])
@jwt_required()
def get_price_analysis(product_id):
    """Get price analysis for a product."""
    try:
        # Lazy import to avoid heavy dependencies at startup
        from services.forecasting import ForecastingService
        forecasting_service = ForecastingService()

        analysis = forecasting_service.get_historical_analysis(product_id)
        
        return jsonify(analysis), 200
    except Exception as e:
        logger.error(f"Error analyzing price history: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to analyze price history"
        }), 500

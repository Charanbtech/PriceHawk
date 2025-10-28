# backend/jobs/tasks.py
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from core.db import get_db
from services.tracking import TrackingService
from services.notifications import NotificationService
# from adapters.base import get_adapter_for_url  # Not implemented yet
from adapters.dev_mock import DevMockAdapter

logger = logging.getLogger(__name__)

def refresh_prices(app):
    """
    Periodic task: Refresh prices for all tracked products.
    
    For each product:
    1. Fetch current price using appropriate adapter
    2. Update price history
    3. Generate notifications if price drops or product is back in stock
    """
    with app.app_context():
        logger.info("Starting price refresh job")
        
        db = get_db()
        tracking_service = TrackingService()
        notification_service = NotificationService()
        
        # Get all products that need to be checked
        # We'll check products that haven't been checked in the last 6 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=6)
        
        products_to_check = list(db.products.find({
            "$or": [
                {"last_checked": {"$lt": cutoff_time}},
                {"last_checked": {"$exists": False}}
            ]
        }))
        
        logger.info(f"Found {len(products_to_check)} products to check")
        
        for product in products_to_check:
            try:
                product_id = product["_id"]
                product_url = product["url"]
                current_price = product["current_price"]
                
                # Get the appropriate adapter for this URL
                # For now, use mock adapter for all URLs
                adapter = DevMockAdapter()
                
                if not adapter:
                    logger.warning(f"No adapter found for URL: {product_url}")
                    continue
                
                # Fetch current product data
                try:
                    product_data = adapter.fetch_product(product_url)
                    
                    if not product_data or "price" not in product_data:
                        logger.warning(f"Failed to fetch price for product {product_id}")
                        continue
                    
                    new_price = product_data["price"]
                    in_stock = product_data.get("in_stock", True)
                    
                except Exception as e:
                    logger.error(f"Error fetching product data: {str(e)}")
                    # If we can't fetch the product, just update the last_checked timestamp
                    db.products.update_one(
                        {"_id": product_id},
                        {"$set": {"last_checked": datetime.utcnow()}}
                    )
                    continue
                
                # Update price and check for notifications
                update_result = tracking_service.update_price(product_id, new_price, in_stock)
                
                # Process notifications
                if update_result["status"] == "success" and update_result.get("notifications"):
                    for notification_data in update_result["notifications"]:
                        # Add product name and image URL to notification
                        notification_data["product_name"] = product["name"]
                        notification_data["image_url"] = product.get("image_url")
                        notification_data["url"] = product["url"]
                        
                        # Create notification
                        notification_service.create_notification(notification_data)
                        
                        # Get user email for email notification
                        user = db.users.find_one({"_id": notification_data["user_id"]})
                        
                        if user and user.get("email") and user.get("notification_preferences", {}).get("email_notifications", True):
                            # Send email notification
                            from api.notifications import send_email
                            
                            subject = f"PriceHawk Alert: {notification_data['type'].replace('_', ' ').title()}"
                            
                            if notification_data["type"] == "price_drop":
                                body = f"""
                                Good news! The price of {product['name']} has dropped.
                                
                                Old price: ${notification_data['old_price']}
                                New price: ${notification_data['new_price']}
                                
                                View the product: {product['url']}
                                
                                - PriceHawk Team
                                """
                            elif notification_data["type"] == "back_in_stock":
                                body = f"""
                                Good news! {product['name']} is back in stock.
                                
                                Current price: ${new_price}
                                
                                View the product: {product['url']}
                                
                                - PriceHawk Team
                                """
                            else:
                                body = notification_data["message"]
                            
                            send_email(user["email"], subject, body)
                
            except Exception as e:
                logger.exception(f"Error refreshing price for product {product.get('_id')}: {str(e)}")
        
        logger.info("Price refresh job completed")

def clean_old_notifications(app):
    """
    Periodic task: Remove notifications older than 30 days.
    """
    with app.app_context():
        logger.info("Starting notification cleanup job")
        
        db = get_db()
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        result = db.notifications.delete_many({
            "created_at": {"$lt": cutoff_date}
        })
        
        logger.info(f"Deleted {result.deleted_count} old notifications")

def generate_price_forecasts(app):
    """
    Periodic task: Generate price forecasts for products with sufficient history.
    """
    with app.app_context():
        logger.info("Starting forecast generation job")
        
        from services.forecasting import ForecastingService
        forecasting_service = ForecastingService()
        
        db = get_db()
        
        # Find products with at least 10 price points
        products = list(db.products.find({
            "price_history.10": {"$exists": True}  # At least 10 price points
        }))
        
        logger.info(f"Generating forecasts for {len(products)} products")
        
        for product in products:
            try:
                product_id = product["_id"]
                
                # Generate forecast
                forecast = forecasting_service.forecast_price(product_id)
                
                if forecast["status"] == "success":
                    # Store forecast data
                    db.forecasts.update_one(
                        {"product_id": product_id},
                        {
                            "$set": {
                                "product_id": product_id,
                                "forecast": forecast["forecast"],
                                "trend": forecast["trend"],
                                "best_buy": forecast["best_buy"],
                                "generated_at": datetime.utcnow()
                            }
                        },
                        upsert=True
                    )
            except Exception as e:
                logger.exception(f"Error generating forecast for product {product.get('_id')}: {str(e)}")
        
        logger.info("Forecast generation job completed")

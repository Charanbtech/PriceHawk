# backend/api/__init__.py
from flask import Blueprint, jsonify, request

def create_api_blueprint():
    api = Blueprint("api", __name__)
    
    print("Creating API blueprint...")
    
    # Register auth blueprint
    try:
        from .auth import bp as auth_bp
        api.register_blueprint(auth_bp, url_prefix="/auth")
        print("✅ Auth blueprint registered")
    except Exception as e:
        print(f"❌ Auth blueprint failed: {e}")
    
    # Register other blueprints
    try:
        from .search import bp as search_bp
        api.register_blueprint(search_bp, url_prefix="/search")
        print("✅ Search blueprint registered")
    except Exception as e:
        print(f"❌ Search blueprint failed: {e}")
    
    try:
        from .tracking import bp as tracking_bp
        api.register_blueprint(tracking_bp, url_prefix="/tracking")
        print("✅ Tracking blueprint registered")
    except Exception as e:
        print(f"❌ Tracking blueprint failed: {e}")
    
    try:
        from .notifications import bp as notifications_bp
        api.register_blueprint(notifications_bp, url_prefix="/notifications")
        print("✅ Notifications blueprint registered")
    except Exception as e:
        print(f"❌ Notifications blueprint failed: {e}")

    # API Health check
    @api.route("/health", methods=["GET"])
    def api_health():
        return jsonify({"status": "ok", "message": "API blueprint working"}), 200
    
    # Database test
    @api.route("/test-db", methods=["GET"])
    def test_database():
        try:
            from core.db import get_db
            db = get_db()
            db.command('ping')
            return jsonify({"status": "success", "message": "DB connected"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @api.route("/search", methods=["POST"])
    def simple_search():
        try:
            from adapters.realtime_adapter import RealtimeAdapter
            from adapters.dev_mock import DevMockAdapter
            
            data = request.get_json() or {}
            query = data.get("query", "")
            max_results = data.get("max_results", 10)
            
            if not query:
                return jsonify({"error": "Query required"}), 400
            
            # Use universal adapter for all products
            from adapters.universal_adapter import UniversalAdapter
            universal_adapter = UniversalAdapter()
            results = universal_adapter.search(query, max_results)
            
            # Add price comparison and recommendations
            mock_adapter = DevMockAdapter()
            recommendations = mock_adapter.get_search_recommendations(query)
            
            # Group results by product and find best prices
            grouped_results = {}
            for result in results:
                product_name = result["title"]
                if product_name not in grouped_results:
                    grouped_results[product_name] = []
                grouped_results[product_name].append(result)
            
            # Add best price indicators
            final_results = []
            for product_name, product_variants in grouped_results.items():
                if len(product_variants) > 1:
                    # Find best price
                    best_price = min(p["price"] for p in product_variants)
                    for variant in product_variants:
                        variant["is_best_price"] = variant["price"] == best_price
                        if variant["is_best_price"]:
                            variant["recommendation"] = "💰 Best Price!"
                        else:
                            savings = variant["price"] - best_price
                            variant["recommendation"] = f"💸 ${savings:.2f} more than best price"
                        final_results.append(variant)
                else:
                    product_variants[0]["is_best_price"] = True
                    product_variants[0]["recommendation"] = "💰 Best Price!"
                    final_results.append(product_variants[0])
            
            return jsonify({"results": final_results, "recommendations": recommendations}), 200
        except Exception as e:
            return jsonify({"error": f"Search failed: {str(e)}"}), 500
    
    # Price prediction endpoint
    @api.route("/predict-price", methods=["POST"])
    def predict_price():
        try:
            import random
            
            data = request.get_json() or {}
            product_name = data.get("product_name", "Product")
            current_price = float(data.get("current_price", 100))
            days_ahead = data.get("days_ahead", 7)
            
            # Generate realistic price prediction
            # Base variation on product type and market trends
            if "iphone" in product_name.lower() or "samsung" in product_name.lower():
                # Electronics tend to decrease over time
                base_trend = -0.02  # -2% base trend
                volatility = 0.05   # 5% volatility
            elif "nike" in product_name.lower() or "adidas" in product_name.lower():
                # Fashion items have seasonal patterns
                base_trend = random.choice([-0.01, 0.01])  # +/-1%
                volatility = 0.08   # 8% volatility
            else:
                # General products
                base_trend = random.uniform(-0.03, 0.02)  # -3% to +2%
                volatility = 0.06   # 6% volatility
            
            # Add random market fluctuation
            market_factor = random.uniform(-volatility, volatility)
            total_change = base_trend + market_factor
            
            # Calculate predicted price
            predicted_price = current_price * (1 + total_change)
            
            # Determine trend and recommendation
            if total_change > 0.01:  # >1% increase
                trend = "increasing"
                recommendation = "Buy now - Price expected to rise"
            elif total_change < -0.01:  # >1% decrease
                trend = "decreasing"
                recommendation = "Wait to buy - Price expected to drop"
            else:
                trend = "stable"
                recommendation = "Price stable - Good time to buy"
            
            return jsonify({
                "status": "success",
                "product_name": product_name,
                "current_price": current_price,
                "predicted_price": round(predicted_price, 2),
                "price_change": round(total_change * 100, 1),
                "trend": trend,
                "recommendation": recommendation,
                "days_ahead": days_ahead
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
    # Real-time price check endpoint
    @api.route("/realtime-price", methods=["POST"])
    def get_realtime_price():
        try:
            data = request.get_json() or {}
            url = data.get("url")
            current_price = float(data.get("current_price", 100))
            
            if not url:
                return jsonify({"error": "URL required"}), 400
            
            # Simulate live price with small variation based on current price
            import random
            variation_percent = random.uniform(-0.05, 0.05)  # +/-5% variation
            live_price = current_price * (1 + variation_percent)
            
            return jsonify({"status": "success", "price": round(live_price, 2), "currency": "$"}), 200
                
        except Exception as e:
            return jsonify({"error": f"Price check failed: {str(e)}"}), 500
    
    # Track product with target price
    @api.route("/track-product", methods=["POST"])
    def track_product():
        try:
            from datetime import datetime
            import uuid
            
            data = request.get_json() or {}
            
            # Create tracking record
            tracking_data = {
                "_id": str(uuid.uuid4()),
                "product_name": data.get("name", "Product"),
                "current_price": float(data.get("current_price", 0)),
                "target_price": float(data.get("target_price", 0)),
                "user_email": data.get("user_email", "user@example.com"),
                "product_url": data.get("url", ""),
                "image_url": data.get("image", ""),
                "platform": data.get("platform", "Unknown"),
                "created_at": datetime.utcnow(),
                "is_active": True,
                "notifications_sent": 0
            }
            
            # Save to database using current_app
            from flask import current_app
            db = current_app.db
            db.tracked_products.insert_one(tracking_data)
            
            return jsonify({
                "status": "success", 
                "message": f"Now tracking {tracking_data['product_name']} for ${tracking_data['target_price']:.2f}!",
                "tracking_id": tracking_data["_id"]
            }), 200
                
        except Exception as e:
            return jsonify({"error": f"Tracking failed: {str(e)}"}), 500
    
    # Get tracked products
    @api.route("/my-products", methods=["GET"])
    def get_my_products():
        try:
            from flask import current_app
            
            db = current_app.db
            products = list(db.tracked_products.find({"is_active": True}).sort("created_at", -1))
            
            return jsonify({"products": products}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to get products: {str(e)}"}), 500
    
    # Get notifications
    @api.route("/my-notifications", methods=["GET"])
    def get_notifications():
        try:
            from flask import current_app
            
            db = current_app.db
            notifications = list(db.notifications.find().sort("created_at", -1).limit(50))
            
            return jsonify({"notifications": notifications}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to get notifications: {str(e)}"}), 500
    
    # Send test email
    @api.route("/send-test-email", methods=["POST"])
    def send_test_email():
        try:
            import smtplib
            from email.mime.text import MIMEText
            import os
            
            data = request.get_json() or {}
            user_email = data.get("email", "user@example.com")
            
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("SENDER_EMAIL_PASSWORD")
            
            # Check if email credentials are configured
            if not sender_email or not sender_password or sender_email == "your-email@gmail.com":
                return jsonify({
                    "status": "error",
                    "message": "Email not configured. Please set SENDER_EMAIL and SENDER_EMAIL_PASSWORD environment variables. See .env.example for setup instructions."
                }), 400
            
            msg = MIMEText("""
🎉 PriceHawk Test Email

This is a test email from PriceHawk price tracking system.

If you receive this email, your notification system is working correctly!

Features:
✅ Price drop alerts
✅ Target price notifications  
✅ Real-time monitoring

Happy price tracking! 🐦💰
            """)
            
            msg['Subject'] = "📧 PriceHawk Test Email - System Working!"
            msg['From'] = sender_email
            msg['To'] = user_email
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                
            return jsonify({
                "status": "success",
                "message": f"Test email sent successfully to {user_email}!"
            }), 200
                
        except Exception as e:
            error_msg = str(e)
            if "Username and Password not accepted" in error_msg:
                return jsonify({
                    "status": "error",
                    "message": "Gmail authentication failed. Please use Gmail App Password (not regular password). Enable 2FA and generate App Password in Gmail settings."
                }), 500
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Email failed: {error_msg}"
                }), 500
    
    # Price monitoring service
    @api.route("/check-prices", methods=["POST"])
    def check_prices():
        try:
            from datetime import datetime
            import random
            import smtplib
            from email.mime.text import MIMEText
            import os
            import uuid
            from flask import current_app
            
            db = current_app.db
            tracked_products = list(db.tracked_products.find({"is_active": True}))
            
            notifications_created = 0
            
            for product in tracked_products:
                # Simulate price check with random variation
                current_price = product["current_price"]
                new_price = current_price + random.uniform(-50, 20)  # Bias towards price drops
                
                # Check if price dropped below target or current price
                price_dropped = new_price < product["target_price"] or new_price < current_price
                
                if price_dropped:
                    # Create notification
                    notification = {
                        "_id": str(uuid.uuid4()),
                        "product_name": product["product_name"],
                        "old_price": current_price,
                        "new_price": new_price,
                        "target_price": product["target_price"],
                        "savings": current_price - new_price,
                        "user_email": product["user_email"],
                        "created_at": datetime.utcnow(),
                        "is_read": False,
                        "type": "price_drop"
                    }
                    
                    db.notifications.insert_one(notification)
                    
                    # Update product price
                    db.tracked_products.update_one(
                        {"_id": product["_id"]},
                        {"$set": {"current_price": new_price}, "$inc": {"notifications_sent": 1}}
                    )
                    
                    # Send email notification
                    try:
                        sender_email = os.getenv("SENDER_EMAIL", "pricehawk@example.com")
                        sender_password = os.getenv("SENDER_EMAIL_PASSWORD", "password")
                        
                        msg = MIMEText(f"""
                        🎉 Great news! The price for {product['product_name']} has dropped!
                        
                        Old Price: ${current_price:.2f}
                        New Price: ${new_price:.2f}
                        Your Target: ${product['target_price']:.2f}
                        You Save: ${notification['savings']:.2f}
                        
                        Check it out now!
                        """)
                        
                        msg['Subject'] = f"💰 Price Drop Alert: {product['product_name']}"
                        msg['From'] = sender_email
                        msg['To'] = product['user_email']
                        
                        with smtplib.SMTP('smtp.gmail.com', 587) as server:
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.send_message(msg)
                            
                    except Exception as email_error:
                        print(f"Email failed: {email_error}")
                    
                    notifications_created += 1
            
            return jsonify({
                "status": "success",
                "message": f"Price check complete. {notifications_created} notifications created.",
                "checked_products": len(tracked_products)
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Price check failed: {str(e)}"}), 500
    
    # Untrack product
    @api.route("/untrack-product/<product_id>", methods=["DELETE"])
    def untrack_product(product_id):
        try:
            from flask import current_app
            
            db = current_app.db
            result = db.tracked_products.update_one(
                {"_id": product_id},
                {"$set": {"is_active": False}}
            )
            
            if result.matched_count > 0:
                return jsonify({"status": "success", "message": "Product untracked"}), 200
            else:
                return jsonify({"error": "Product not found"}), 404
                
        except Exception as e:
            return jsonify({"error": f"Untrack failed: {str(e)}"}), 500
    
    # Update target price
    @api.route("/update-target-price/<product_id>", methods=["PATCH"])
    def update_target_price(product_id):
        try:
            from flask import current_app
            
            data = request.get_json() or {}
            new_target_price = float(data.get("target_price", 0))
            
            if new_target_price <= 0:
                return jsonify({"error": "Invalid target price"}), 400
            
            db = current_app.db
            result = db.tracked_products.update_one(
                {"_id": product_id},
                {"$set": {"target_price": new_target_price}}
            )
            
            if result.matched_count > 0:
                return jsonify({"status": "success", "message": "Target price updated"}), 200
            else:
                return jsonify({"error": "Product not found"}), 404
                
        except Exception as e:
            return jsonify({"error": f"Update failed: {str(e)}"}), 500
    
    print("API blueprint created successfully")
    return api
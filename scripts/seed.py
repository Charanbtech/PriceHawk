#!/usr/bin/env python3
# scripts/seed.py
"""
Seed script for PriceHawk database.
Creates sample users, products, and tracking data for testing.
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import create_app
from core.security import hash_password

def seed_database():
    app = create_app()
    
    with app.app_context():
        db = app.db
        
        print("🌱 Seeding PriceHawk database...")
        
        # Clear existing data
        print("Clearing existing data...")
        db.users.delete_many({})
        db.products.delete_many({})
        db.user_tracking.delete_many({})
        db.notifications.delete_many({})
        
        # Create sample users
        print("Creating sample users...")
        users = [
            {
                "email": "demo@pricehawk.com",
                "password": hash_password("password123"),
                "name": "Demo User",
                "created_at": datetime.utcnow()
            },
            {
                "email": "john@example.com",
                "password": hash_password("password123"),
                "name": "John Doe",
                "created_at": datetime.utcnow()
            }
        ]
        
        user_ids = []
        for user in users:
            user_id = db.users.insert_one(user).inserted_id
            user_ids.append(user_id)
            print(f"  ✓ Created user: {user['email']}")
        
        # Create sample products with price history
        print("Creating sample products...")
        products = [
            {
                "name": "iPhone 15 Pro 128GB",
                "url": "https://example.com/iphone-15-pro",
                "image_url": "https://via.placeholder.com/300x200?text=iPhone+15+Pro",
                "description": "Latest iPhone with Pro features",
                "current_price": 999.99,
                "original_price": 1099.99,
                "currency": "$",
                "source": "Apple Store",
                "category": "Electronics",
                "in_stock": True,
                "created_at": datetime.utcnow() - timedelta(days=30),
                "last_checked": datetime.utcnow(),
                "price_history": [
                    {"price": 1099.99, "date": datetime.utcnow() - timedelta(days=30)},
                    {"price": 1079.99, "date": datetime.utcnow() - timedelta(days=25)},
                    {"price": 1049.99, "date": datetime.utcnow() - timedelta(days=20)},
                    {"price": 1029.99, "date": datetime.utcnow() - timedelta(days=15)},
                    {"price": 1009.99, "date": datetime.utcnow() - timedelta(days=10)},
                    {"price": 999.99, "date": datetime.utcnow() - timedelta(days=5)},
                ]
            },
            {
                "name": "Sony WH-1000XM5 Headphones",
                "url": "https://example.com/sony-headphones",
                "image_url": "https://via.placeholder.com/300x200?text=Sony+Headphones",
                "description": "Premium noise-canceling headphones",
                "current_price": 349.99,
                "original_price": 399.99,
                "currency": "$",
                "source": "Best Buy",
                "category": "Audio",
                "in_stock": True,
                "created_at": datetime.utcnow() - timedelta(days=20),
                "last_checked": datetime.utcnow(),
                "price_history": [
                    {"price": 399.99, "date": datetime.utcnow() - timedelta(days=20)},
                    {"price": 379.99, "date": datetime.utcnow() - timedelta(days=15)},
                    {"price": 359.99, "date": datetime.utcnow() - timedelta(days=10)},
                    {"price": 349.99, "date": datetime.utcnow() - timedelta(days=5)},
                ]
            },
            {
                "name": "MacBook Pro 14-inch M3",
                "url": "https://example.com/macbook-pro",
                "image_url": "https://via.placeholder.com/300x200?text=MacBook+Pro",
                "description": "Professional laptop with M3 chip",
                "current_price": 1999.99,
                "original_price": 1999.99,
                "currency": "$",
                "source": "Apple Store",
                "category": "Computers",
                "in_stock": False,
                "created_at": datetime.utcnow() - timedelta(days=15),
                "last_checked": datetime.utcnow(),
                "price_history": [
                    {"price": 1999.99, "date": datetime.utcnow() - timedelta(days=15)},
                    {"price": 1999.99, "date": datetime.utcnow() - timedelta(days=10)},
                    {"price": 1999.99, "date": datetime.utcnow() - timedelta(days=5)},
                ]
            }
        ]
        
        product_ids = []
        for product in products:
            product_id = db.products.insert_one(product).inserted_id
            product_ids.append(product_id)
            print(f"  ✓ Created product: {product['name']}")
        
        # Create sample tracking records
        print("Creating sample tracking records...")
        tracking_records = [
            {
                "user_id": str(user_ids[0]),
                "product_id": product_ids[0],
                "target_price": 950.00,
                "notify_on_price_drop": True,
                "notify_on_availability": True,
                "created_at": datetime.utcnow() - timedelta(days=25)
            },
            {
                "user_id": str(user_ids[0]),
                "product_id": product_ids[1],
                "target_price": 320.00,
                "notify_on_price_drop": True,
                "notify_on_availability": True,
                "created_at": datetime.utcnow() - timedelta(days=15)
            },
            {
                "user_id": str(user_ids[1]),
                "product_id": product_ids[2],
                "target_price": 1800.00,
                "notify_on_price_drop": True,
                "notify_on_availability": True,
                "created_at": datetime.utcnow() - timedelta(days=10)
            }
        ]
        
        for record in tracking_records:
            db.user_tracking.insert_one(record)
            print(f"  ✓ Created tracking record for user {record['user_id']}")
        
        # Create sample notifications
        print("Creating sample notifications...")
        notifications = [
            {
                "user_id": str(user_ids[0]),
                "type": "price_drop",
                "message": "iPhone 15 Pro price dropped from $1099.99 to $999.99!",
                "product_id": str(product_ids[0]),
                "product_name": "iPhone 15 Pro 128GB",
                "old_price": 1099.99,
                "new_price": 999.99,
                "url": "https://example.com/iphone-15-pro",
                "read": False,
                "created_at": datetime.utcnow() - timedelta(days=5)
            },
            {
                "user_id": str(user_ids[0]),
                "type": "price_drop",
                "message": "Sony WH-1000XM5 price dropped from $399.99 to $349.99!",
                "product_id": str(product_ids[1]),
                "product_name": "Sony WH-1000XM5 Headphones",
                "old_price": 399.99,
                "new_price": 349.99,
                "url": "https://example.com/sony-headphones",
                "read": True,
                "created_at": datetime.utcnow() - timedelta(days=10)
            },
            {
                "user_id": str(user_ids[1]),
                "type": "back_in_stock",
                "message": "MacBook Pro 14-inch M3 is back in stock!",
                "product_id": str(product_ids[2]),
                "product_name": "MacBook Pro 14-inch M3",
                "url": "https://example.com/macbook-pro",
                "read": False,
                "created_at": datetime.utcnow() - timedelta(days=2)
            }
        ]
        
        for notification in notifications:
            db.notifications.insert_one(notification)
            print(f"  ✓ Created notification: {notification['type']}")
        
        print("\n🎉 Database seeded successfully!")
        print(f"\n📊 Summary:")
        print(f"  Users: {len(users)}")
        print(f"  Products: {len(products)}")
        print(f"  Tracking Records: {len(tracking_records)}")
        print(f"  Notifications: {len(notifications)}")
        print(f"\n🔑 Test Credentials:")
        print(f"  Email: demo@pricehawk.com")
        print(f"  Password: password123")
        print(f"\n  Email: john@example.com")
        print(f"  Password: password123")

if __name__ == "__main__":
    seed_database()

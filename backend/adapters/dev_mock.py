# backend/adapters/dev_mock.py
from .base import BaseAdapter
import random
import time
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class DevMockAdapter(BaseAdapter):
    def __init__(self, source_name="dev_mock"):
        self.source = source_name
        # Initialize semantic matching model
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except:
            self.model = None  # Fallback if model not available

    def search(self, query: str, max_results: int = 5):
        now = int(time.time())
        results = []
        
        # Enhanced product database with real URLs (Amazon & Flipkart only)
        product_database = [
            # iPhone 16 Series
            {"name": "Apple iPhone 16 Pro 256GB Natural Titanium", "amazon": 1199.99, "flipkart": 1149.99, "rating": 4.8, "reviews": 850, "amazon_url": "https://www.amazon.com/Apple-iPhone-256GB-Natural-Titanium/dp/B0DGHXM2CX", "flipkart_url": "https://www.flipkart.com/apple-iphone-16-pro-natural-titanium-256-gb/p/itm6c6d4c5b5c5e5"},
            {"name": "iPhone 16 128GB Black", "amazon": 999.99, "flipkart": 979.99, "rating": 4.6, "reviews": 1200, "amazon_url": "https://www.amazon.com/Apple-iPhone-16-128GB-Black/dp/B0DGHXM3RT", "flipkart_url": "https://www.flipkart.com/apple-iphone-16-black-128-gb/p/itm7d7e5d6f6d6f6"},
            
            # iPhone 15 Series
            {"name": "Apple iPhone 15 Pro 128GB Blue Titanium", "amazon": 899.99, "flipkart": 879.99, "rating": 4.5, "reviews": 1250, "amazon_url": "https://www.amazon.com/Apple-iPhone-15-Pro-128GB/dp/B0CHX1W1XY", "flipkart_url": "https://www.flipkart.com/apple-iphone-15-pro-blue-titanium-128-gb/p/itm8e8f6e7g7e7g7"},
            {"name": "iPhone 15 256GB Pink", "amazon": 799.99, "flipkart": 789.99, "rating": 4.3, "reviews": 890, "amazon_url": "https://www.amazon.com/Apple-iPhone-15-256GB-Pink/dp/B0CHX2W2YZ", "flipkart_url": "https://www.flipkart.com/apple-iphone-15-pink-256-gb/p/itm9f9g7f8h8f8h8"},
            
            # iPhone 14 Series
            {"name": "Apple iPhone 14 Pro 128GB Deep Purple", "amazon": 699.99, "flipkart": 679.99, "rating": 4.6, "reviews": 2100, "amazon_url": "https://www.amazon.com/Apple-iPhone-14-Pro-128GB/dp/B0BN72FYFG", "flipkart_url": "https://www.flipkart.com/apple-iphone-14-pro-deep-purple-128-gb/p/itma0a1h8a2i9a2i"},
            {"name": "iPhone 14 128GB Blue", "amazon": 599.99, "flipkart": 589.99, "rating": 4.4, "reviews": 1800, "amazon_url": "https://www.amazon.com/Apple-iPhone-14-128GB-Blue/dp/B0BN72FYGG", "flipkart_url": "https://www.flipkart.com/apple-iphone-14-blue-128-gb/p/itmb1b2i9b3j0b3j"},
            
            # Samsung Galaxy Series
            {"name": "Samsung Galaxy S24 Ultra 256GB Titanium Gray", "amazon": 1299.99, "flipkart": 1249.99, "rating": 4.7, "reviews": 950, "amazon_url": "https://www.amazon.com/Samsung-Galaxy-S24-Ultra-256GB/dp/B0CMDM1PY2", "flipkart_url": "https://www.flipkart.com/samsung-galaxy-s24-ultra-titanium-gray-256-gb/p/itmc2c3j0c4k1c4k"},
            {"name": "Galaxy S23 128GB Phantom Black", "amazon": 799.99, "flipkart": 779.99, "rating": 4.5, "reviews": 1400, "amazon_url": "https://www.amazon.com/Samsung-Galaxy-S23-128GB-Phantom/dp/B0BLP4JQZ6", "flipkart_url": "https://www.flipkart.com/samsung-galaxy-s23-phantom-black-128-gb/p/itmd3d4k1d5l2d5l"}
        ]
        
        # Semantic product matching using sentence transformers
        matching_products = []
        
        if self.model:
            # Use semantic matching
            query_embedding = self.model.encode([query])
            product_names = [p["name"] for p in product_database]
            product_embeddings = self.model.encode(product_names)
            
            # Calculate similarity scores
            similarities = cosine_similarity(query_embedding, product_embeddings)[0]
            
            # Get products with similarity > 0.3 (30%)
            for i, similarity in enumerate(similarities):
                if similarity > 0.3:
                    product = product_database[i]
                    sources = ["amazon", "flipkart"]
                    prices = {source: product.get(source, 999.99) for source in sources}
                    
                    # Find best price and source
                    best_source = min(prices, key=prices.get)
                    best_price = prices[best_source]
                    
                    # Create entries for each source
                    for source in sources:
                        if source in product:
                            matching_products.append({
                                "name": product["name"],
                                "price": product[source],
                                "source": source.replace("_", " ").title(),
                                "rating": product["rating"],
                                "reviews": product["reviews"],
                                "is_best_price": source == best_source,
                                "savings": round(product[source] - best_price, 2) if source != best_source else 0,
                                "similarity": similarity,
                                "url_key": f"{source}_url"
                            })
        else:
            # Fallback to keyword matching
            query_lower = query.lower()
            for product in product_database:
                if any(word in product["name"].lower() for word in query_lower.split()):
                    sources = ["amazon", "flipkart"]
                    prices = {source: product.get(source, 999.99) for source in sources}
                    
                    best_source = min(prices, key=prices.get)
                    best_price = prices[best_source]
                    
                    for source in sources:
                        if source in product:
                            matching_products.append({
                                "name": product["name"],
                                "price": product[source],
                                "source": source.replace("_", " ").title(),
                                "rating": product["rating"],
                                "reviews": product["reviews"],
                                "is_best_price": source == best_source,
                                "savings": round(product[source] - best_price, 2) if source != best_source else 0,
                                "similarity": 0.8,
                                "url_key": f"{source}_url"
                            })
        
        # Sort by similarity and best price
        matching_products.sort(key=lambda x: (-x.get("similarity", 0), x["price"]))
        
        # Build final results with price comparison info
        for i, product in enumerate(matching_products[:max_results]):
            # Get real product URL from database
            source_name = product.get("source", "Amazon")
            url_key = product.get("url_key", "amazon_url")
            
            # Find the original product in database to get URL
            product_url = "https://example.com/product-not-found"
            for db_product in product_database:
                if db_product["name"] == product["name"]:
                    product_url = db_product.get(url_key, product_url)
                    break
            
            result = {
                "title": product["name"],
                "price": round(product["price"], 2),
                "currency": "$",
                "url": product_url,
                "source": source_name,
                "product_id": f"mock-{i}-{now}",
                "image_url": f"https://via.placeholder.com/300x200?text={product['name'].replace(' ', '+')}",
                "description": f"High-quality {product['name']} with excellent features and performance.",
                "rating": product.get("rating", 4.0),
                "review_count": product.get("reviews", 100),
                "in_stock": random.choice([True, True, True, False]),
                "category": query.split()[0] if query else "Electronics",
                "is_best_price": product.get("is_best_price", False),
                "savings_vs_best": product.get("savings", 0)
            }
            
            # Add recommendation badge for best price
            if product.get("is_best_price"):
                result["recommendation"] = "💰 Best Price!"
            elif product.get("savings", 0) > 0:
                result["recommendation"] = f"💸 ${product['savings']:.2f} more than best price"
            
            results.append(result)
        
        return results

    def get_search_recommendations(self, query: str):
        """Generate search recommendations based on query"""
        query_lower = query.lower()
        recommendations = []
        
        if "iphone 16" in query_lower:
            recommendations = [
                "iPhone 16 Pro 128GB", "iPhone 16 Pro 256GB", "iPhone 16 Pro 512GB",
                "iPhone 16 128GB", "iPhone 16 256GB", "iPhone 16 512GB",
                "iPhone 16 Pro Natural Titanium", "iPhone 16 Pro Blue Titanium",
                "iPhone 16 Black", "iPhone 16 White", "iPhone 16 Pink"
            ]
        elif "iphone 15" in query_lower:
            recommendations = [
                "iPhone 15 Pro 128GB", "iPhone 15 Pro 256GB", "iPhone 15 Pro 512GB",
                "iPhone 15 128GB", "iPhone 15 256GB", "iPhone 15 512GB",
                "iPhone 15 Pro Blue Titanium", "iPhone 15 Pro Natural Titanium",
                "iPhone 15 Pink", "iPhone 15 Blue", "iPhone 15 Green"
            ]
        elif "iphone 14" in query_lower:
            recommendations = [
                "iPhone 14 Pro 128GB", "iPhone 14 Pro 256GB", "iPhone 14 Pro 512GB",
                "iPhone 14 128GB", "iPhone 14 256GB", "iPhone 14 512GB",
                "iPhone 14 Pro Deep Purple", "iPhone 14 Pro Space Black",
                "iPhone 14 Blue", "iPhone 14 Purple", "iPhone 14 Midnight"
            ]
        elif "samsung" in query_lower or "galaxy" in query_lower:
            recommendations = [
                "Galaxy S24 Ultra 256GB", "Galaxy S24 Ultra 512GB", "Galaxy S24 Ultra 1TB",
                "Galaxy S23 128GB", "Galaxy S23 256GB", "Galaxy S23 512GB",
                "Galaxy S24 Titanium Gray", "Galaxy S24 Titanium Black",
                "Galaxy S23 Phantom Black", "Galaxy S23 Cream", "Galaxy S23 Green"
            ]
        elif "washing machine" in query_lower:
            recommendations = [
                "LG Front Load Washing Machine", "Samsung Top Load Washing Machine",
                "Whirlpool Semi Automatic", "Bosch 7kg Washing Machine",
                "IFB 6kg Front Load", "Godrej 6.5kg Top Load"
            ]
        elif "laptop" in query_lower:
            recommendations = [
                "Dell Inspiron 15", "HP Pavilion 14", "Lenovo ThinkPad",
                "MacBook Air M2", "MacBook Pro M3", "ASUS VivoBook"
            ]
        elif "headphones" in query_lower:
            recommendations = [
                "Sony WH-1000XM5", "Apple AirPods Pro", "JBL Tune 760NC",
                "Bose QuietComfort", "Sennheiser HD 450BT"
            ]
        elif "iphone" in query_lower:
            recommendations = [
                "iPhone 16 Pro", "iPhone 15 Pro", "iPhone 14 Pro",
                "iPhone 16 128GB", "iPhone 15 256GB", "iPhone 14 512GB",
                "iPhone Pro Max", "iPhone Mini", "iPhone Plus"
            ]
        
        return recommendations[:8]  # Limit to 8 recommendations

    def fetch_price_history(self, product_id: str):
        # mock time-series
        import pandas as pd
        import numpy as np
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30).tolist()
        history = [{"date": str(d.date()), "price": round(100 + i*random.uniform(-2, 2), 2)} for i, d in enumerate(dates)]
        return history

    def fetch_product(self, url: str):
        return {
            "title": "Mock product from URL",
            "price": 199.99,
            "currency": "$",
            "url": url,
            "source": self.source,
            "product_id": "mock-url-1",
            "image_url": "https://via.placeholder.com/300x200?text=Mock+Product",
            "description": "This is a mock product fetched from URL for testing purposes.",
            "rating": 4.2,
            "review_count": 156,
            "in_stock": True,
            "category": "Electronics"
        }
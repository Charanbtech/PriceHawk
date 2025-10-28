# backend/adapters/universal_adapter.py
from .base import BaseAdapter
import random
import time

class UniversalAdapter(BaseAdapter):
    def __init__(self):
        # Comprehensive product database covering all categories
        self.products = {
            # Electronics - Smartphones
            "iphone": [
                {"name": "Apple iPhone 15 Pro 128GB", "amazon": 999, "flipkart": 979, "rating": 4.5, "reviews": 1250},
                {"name": "Apple iPhone 16 128GB", "amazon": 799, "flipkart": 779, "rating": 4.6, "reviews": 890},
                {"name": "Apple iPhone 14 Pro 128GB", "amazon": 699, "flipkart": 679, "rating": 4.4, "reviews": 2100}
            ],
            "samsung": [
                {"name": "Samsung Galaxy S24 Ultra 256GB", "amazon": 1199, "flipkart": 1149, "rating": 4.4, "reviews": 567},
                {"name": "Samsung Galaxy S23 128GB", "amazon": 799, "flipkart": 779, "rating": 4.3, "reviews": 890},
                {"name": "Samsung Galaxy A54 128GB", "amazon": 399, "flipkart": 379, "rating": 4.2, "reviews": 1200}
            ],
            
            # Home Appliances
            "washing machine": [
                {"name": "LG 7kg Front Load Washing Machine", "amazon": 599, "flipkart": 579, "rating": 4.3, "reviews": 850},
                {"name": "Samsung 6.5kg Top Load Washing Machine", "amazon": 399, "flipkart": 389, "rating": 4.2, "reviews": 1200},
                {"name": "Whirlpool 8kg Semi Automatic Washing Machine", "amazon": 299, "flipkart": 279, "rating": 4.1, "reviews": 950}
            ],
            "refrigerator": [
                {"name": "LG 260L Double Door Refrigerator", "amazon": 799, "flipkart": 779, "rating": 4.4, "reviews": 650},
                {"name": "Samsung 236L Single Door Refrigerator", "amazon": 599, "flipkart": 579, "rating": 4.2, "reviews": 890},
                {"name": "Whirlpool 340L Triple Door Refrigerator", "amazon": 1199, "flipkart": 1149, "rating": 4.5, "reviews": 420}
            ],
            "air conditioner": [
                {"name": "LG 1.5 Ton Split AC", "amazon": 899, "flipkart": 879, "rating": 4.3, "reviews": 750},
                {"name": "Samsung 1 Ton Window AC", "amazon": 599, "flipkart": 579, "rating": 4.1, "reviews": 650},
                {"name": "Daikin 2 Ton Split AC", "amazon": 1299, "flipkart": 1249, "rating": 4.6, "reviews": 380}
            ],
            
            # Electronics - Laptops & Computers
            "laptop": [
                {"name": "Dell Inspiron 15 3000 Core i5", "amazon": 899, "flipkart": 879, "rating": 4.2, "reviews": 1200},
                {"name": "HP Pavilion 14 AMD Ryzen 5", "amazon": 799, "flipkart": 779, "rating": 4.3, "reviews": 950},
                {"name": "Lenovo ThinkPad E14 Intel i7", "amazon": 1299, "flipkart": 1249, "rating": 4.5, "reviews": 680}
            ],
            "macbook": [
                {"name": "MacBook Air M2 256GB", "amazon": 1199, "flipkart": 1149, "rating": 4.7, "reviews": 850},
                {"name": "MacBook Pro 14 M3 512GB", "amazon": 1999, "flipkart": 1949, "rating": 4.8, "reviews": 420},
                {"name": "MacBook Air M1 256GB", "amazon": 999, "flipkart": 979, "rating": 4.6, "reviews": 1200}
            ],
            
            # Fashion & Clothing
            "shoes": [
                {"name": "Nike Air Max 270 Running Shoes", "amazon": 129, "flipkart": 119, "rating": 4.4, "reviews": 2200},
                {"name": "Adidas Ultraboost 22 Sneakers", "amazon": 179, "flipkart": 169, "rating": 4.5, "reviews": 1800},
                {"name": "Puma RS-X Sports Shoes", "amazon": 99, "flipkart": 89, "rating": 4.2, "reviews": 1500}
            ],
            "shirt": [
                {"name": "Levi's Classic Cotton Shirt", "amazon": 49, "flipkart": 45, "rating": 4.3, "reviews": 950},
                {"name": "Arrow Formal White Shirt", "amazon": 39, "flipkart": 35, "rating": 4.2, "reviews": 1200},
                {"name": "Tommy Hilfiger Casual Shirt", "amazon": 79, "flipkart": 75, "rating": 4.4, "reviews": 680}
            ],
            
            # Books & Education
            "book": [
                {"name": "The Psychology of Money", "amazon": 15, "flipkart": 12, "rating": 4.6, "reviews": 5200},
                {"name": "Atomic Habits by James Clear", "amazon": 18, "flipkart": 16, "rating": 4.7, "reviews": 8900},
                {"name": "Think and Grow Rich", "amazon": 12, "flipkart": 10, "rating": 4.5, "reviews": 3200}
            ],
            
            # Sports & Fitness
            "headphones": [
                {"name": "Sony WH-1000XM5 Wireless Headphones", "amazon": 399, "flipkart": 379, "rating": 4.6, "reviews": 1200},
                {"name": "Apple AirPods Pro 2nd Gen", "amazon": 249, "flipkart": 239, "rating": 4.5, "reviews": 2100},
                {"name": "JBL Tune 760NC Headphones", "amazon": 99, "flipkart": 89, "rating": 4.2, "reviews": 1800}
            ],
            
            # Kitchen Appliances
            "microwave": [
                {"name": "LG 28L Convection Microwave", "amazon": 299, "flipkart": 279, "rating": 4.3, "reviews": 850},
                {"name": "Samsung 23L Solo Microwave", "amazon": 199, "flipkart": 189, "rating": 4.1, "reviews": 1200},
                {"name": "IFB 30L Convection Microwave", "amazon": 399, "flipkart": 379, "rating": 4.4, "reviews": 650}
            ]
        }
        
    def search(self, query: str, max_results: int = 10):
        results = []
        now = int(time.time())
        query_lower = query.lower()
        
        # Find matching products
        matching_products = []
        
        for category, products in self.products.items():
            # Check if query matches category or product names
            if category in query_lower or any(word in category for word in query_lower.split()):
                matching_products.extend(products)
            else:
                # Check individual product names
                for product in products:
                    if any(word in product["name"].lower() for word in query_lower.split()):
                        matching_products.append(product)
        
        # If no matches, create generic results
        if not matching_products:
            matching_products = [
                {"name": f"{query.title()} - Premium Model", "amazon": random.randint(100, 800), "flipkart": random.randint(90, 750), "rating": 4.2, "reviews": 150},
                {"name": f"{query.title()} - Standard Model", "amazon": random.randint(50, 400), "flipkart": random.randint(45, 380), "rating": 4.0, "reviews": 89}
            ]
        
        # Create results for both Amazon and Flipkart
        for product in matching_products[:max_results//2]:
            # Generate search URLs
            search_term = query.replace(" ", "+")
            
            # Amazon result
            results.append({
                "title": product["name"],
                "price": product["amazon"],
                "currency": "$",
                "url": f"https://www.amazon.com/s?k={search_term}",
                "source": "Amazon",
                "product_id": f"amazon-{len(results)}-{now}",
                "image_url": "https://via.placeholder.com/300x200?text=" + product["name"].replace(" ", "+"),
                "description": f"Genuine {product['name']} from Amazon with fast shipping.",
                "rating": product["rating"],
                "review_count": product["reviews"],
                "in_stock": True,
                "category": "Electronics"
            })
            
            # Flipkart result
            results.append({
                "title": product["name"],
                "price": product["flipkart"],
                "currency": "$",
                "url": f"https://www.flipkart.com/search?q={search_term}",
                "source": "Flipkart",
                "product_id": f"flipkart-{len(results)}-{now}",
                "image_url": "https://via.placeholder.com/300x200?text=" + product["name"].replace(" ", "+"),
                "description": f"Authentic {product['name']} from Flipkart with warranty.",
                "rating": product["rating"],
                "review_count": product["reviews"],
                "in_stock": True,
                "category": "Electronics"
            })
        
        return results[:max_results]
    
    def fetch_price_history(self, product_id: str):
        return []
    
    def fetch_product(self, url: str):
        return {
            "title": "Product from URL",
            "price": 299.99,
            "currency": "$",
            "url": url,
            "source": "Direct",
            "product_id": "direct-1",
            "image_url": "",
            "description": "Product fetched from URL",
            "rating": 4.0,
            "review_count": 100,
            "in_stock": True,
            "category": "Electronics"
        }
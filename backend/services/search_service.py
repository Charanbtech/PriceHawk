# backend/services/search_service.py
from typing import List
from core.schemas import ProductSearchIn, ProductOut
import random

def search_products(payload: ProductSearchIn) -> List[ProductOut]:
    """
    Mock product search service.
    Later this can integrate with Amazon/Flipkart scrapers or APIs.
    """
    sample_products = [
        {
            "title": f"{payload.query} - Amazon Edition",
            "price": round(random.uniform(5000, 80000), 2),
            "currency": "INR",
            "url": f"https://www.amazon.in/s?k={payload.query}",
            "source": "Amazon"
        },
        {
            "title": f"{payload.query} - Flipkart Edition",
            "price": round(random.uniform(5000, 80000), 2),
            "currency": "INR",
            "url": f"https://www.flipkart.com/search?q={payload.query}",
            "source": "Flipkart"
        }
    ]

    # Convert dicts → ProductOut Pydantic objects
    return [ProductOut(**p) for p in sample_products[:payload.max_results]]

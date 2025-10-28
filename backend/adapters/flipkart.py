# backend/adapters/flipkart.py
from .base import BaseAdapter

class FlipkartAdapter(BaseAdapter):
    def __init__(self):
        self.source = "flipkart"
    def search(self, query: str, max_results: int = 10):
        # TODO: Integrate Flipkart affiliate API
        raise NotImplementedError("Use Flipkart affiliate API.")
    def fetch_price_history(self, product_id: str):
        raise NotImplementedError
    def fetch_product(self, url: str):
        raise NotImplementedError

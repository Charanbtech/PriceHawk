# backend/adapters/amazon.py
from .base import BaseAdapter

class AmazonAdapter(BaseAdapter):
    def __init__(self):
        self.source = "amazon"
    def search(self, query: str, max_results: int = 10):
        # TODO: Connect to Amazon PAAPI or use approved affiliate API
        raise NotImplementedError("Use Amazon Product Advertising API or approved source.")
    def fetch_price_history(self, product_id: str):
        raise NotImplementedError
    def fetch_product(self, url: str):
        raise NotImplementedError

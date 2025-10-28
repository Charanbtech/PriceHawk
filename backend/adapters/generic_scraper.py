# backend/adapters/generic_scraper.py
from .base import BaseAdapter
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

class GenericScraper(BaseAdapter):
    def __init__(self, source_name="generic"):
        self.source = source_name
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        # Placeholder: implement Playwright or requests+BS4 logic per site
        # Raise NotImplementedError to remind you to implement
        raise NotImplementedError("GenericScraper.search must be implemented per target site.")
    def fetch_price_history(self, product_id: str):
        raise NotImplementedError
    def fetch_product(self, url: str) -> Dict:
        raise NotImplementedError

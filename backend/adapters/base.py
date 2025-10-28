# backend/adapters/base.py
from abc import ABC, abstractmethod
from typing import List, Dict

class BaseAdapter(ABC):
    """Base adapter interface for scrapers."""

    @abstractmethod
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        pass

    @abstractmethod
    def fetch_price_history(self, product_id: str):
        pass

    @abstractmethod
    def fetch_product(self, url: str) -> Dict:
        pass

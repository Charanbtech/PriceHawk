# backend/services/comparison.py
from typing import List, Dict
from services.matching import cluster_products

def find_best_deals(items: List[Dict]) -> List[Dict]:
    """
    Return best deal per cluster of similar products.
    """
    clusters = cluster_products(items, score_threshold=0.7)
    best = []
    for grp in clusters:
        sorted_grp = sorted(grp, key=lambda x: x.get("price", float("inf")))
        best.append(sorted_grp[0])
    return best

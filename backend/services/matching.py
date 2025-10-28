# backend/services/matching.py
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer, util
    try:
        MODEL = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("✅ Sentence Transformers model loaded successfully")
    except Exception as e:
        logger.warning(f"⚠️ Could not load sentence transformers model: {e}")
        MODEL = None
except ImportError:
    logger.warning("⚠️ sentence_transformers not installed - using fallback clustering")
    MODEL = None
    util = None

def embed_texts(texts: List[str]):
    """
    Convert texts to embeddings using sentence transformers.
    Falls back to simple lowercase for fallback.
    """
    if not MODEL:
        return [t.lower() for t in texts]
    return MODEL.encode(texts, convert_to_tensor=True)

def get_similarity_score(text1: str, text2: str) -> float:
    """
    Calculate similarity score between two texts (0-1).
    """
    if not MODEL:
        return 1.0 if text1.lower() == text2.lower() else 0.0
    
    try:
        embeddings = MODEL.encode([text1, text2], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
        return float(similarity)
    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        return 0.0

def cluster_products(items: List[Dict], score_threshold: float = 0.75) -> List[List[Dict]]:
    """
    Group similar products by title using embeddings.
    
    Args:
        items: List of products with 'title' field
        score_threshold: Minimum similarity score to group items (0-1)
    
    Returns:
        List of clusters, where each cluster is a list of similar items
    """
    if not items:
        return []
    
    if len(items) == 1:
        return [items]
    
    titles = [i.get("title", "") for i in items]
    
    if MODEL:
        try:
            embeddings = MODEL.encode(titles, convert_to_tensor=True)
            import numpy as np
            
            clusters = []
            used = set()
            sims = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()
            
            for i in range(len(titles)):
                if i in used:
                    continue
                    
                group = [items[i]]
                used.add(i)
                
                for j in range(i + 1, len(titles)):
                    if j in used:
                        continue
                    if sims[i, j] >= score_threshold:
                        group.append(items[j])
                        used.add(j)
                
                clusters.append(group)
            
            return clusters
        except Exception as e:
            logger.error(f"Error in clustering with embeddings: {e}")
            return fallback_cluster_products(items)
    else:
        return fallback_cluster_products(items)

def fallback_cluster_products(items: List[Dict]) -> List[List[Dict]]:
    """
    Fallback clustering when sentence transformers is not available.
    Groups by lowercased title prefix.
    """
    mapped = {}
    for item in items:
        title = item.get("title", "").lower()
        key = title.split("-")[0].strip() if "-" in title else title.split()[0] if title else "unknown"
        if not key:
            key = "unknown"
        mapped.setdefault(key, []).append(item)
    return list(mapped.values())

def find_best_price_in_cluster(cluster: List[Dict]) -> Dict:
    """
    Find the product with the lowest price in a cluster.
    """
    if not cluster:
        return None
    
    best = min(cluster, key=lambda x: x.get("price", float('inf')))
    return best

def get_cluster_summary(cluster: List[Dict]) -> Dict:
    """
    Get summary statistics for a product cluster.
    """
    if not cluster:
        return None
    
    prices = [item.get("price", 0) for item in cluster]
    ratings = [item.get("rating", 0) for item in cluster if item.get("rating")]
    
    return {
        "count": len(cluster),
        "min_price": min(prices),
        "max_price": max(prices),
        "avg_price": sum(prices) / len(prices),
        "avg_rating": sum(ratings) / len(ratings) if ratings else 0,
        "sources": list(set(item.get("source", "unknown") for item in cluster)),
        "best_price_product": find_best_price_in_cluster(cluster)
    }

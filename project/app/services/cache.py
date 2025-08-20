import time
import hashlib
import json
from typing import Any, Optional
from collections import OrderedDict
from app.config import settings

class LRUCache:
    """Simple in-memory LRU cache with TTL"""
    
    def __init__(self, capacity: int = 1000, ttl_seconds: int = 600):
        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
            
        value, timestamp = self.cache[key]
        
        # Check if expired
        if time.time() - timestamp > self.ttl_seconds:
            self.cache.pop(key)
            return None
            
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return value
    
    def set(self, key: str, value: Any) -> None:
        # Remove oldest if at capacity
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
            
        self.cache[key] = (value, time.time())
    
    def clear(self) -> None:
        self.cache.clear()

class CacheManager:
    """Manages different cache types"""
    
    def __init__(self):
        self.response_cache = LRUCache(
            capacity=500, 
            ttl_seconds=settings.cache_ttl_seconds
        )
        self.embedding_cache = LRUCache(
            capacity=10000, 
            ttl_seconds=settings.embedding_cache_ttl
        )
    
    def generate_key(self, prefix: str, data: dict) -> str:
        """Generate consistent cache key from data"""
        serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
        hash_obj = hashlib.sha256(serialized.encode())
        return f"{prefix}:{hash_obj.hexdigest()[:16]}"
    
    def get_response(self, key: str) -> Optional[dict]:
        return self.response_cache.get(key)
    
    def set_response(self, key: str, response: dict) -> None:
        self.response_cache.set(key, response)
    
    def get_embedding(self, text_hash: str) -> Optional[Any]:
        return self.embedding_cache.get(f"emb:{text_hash}")
    
    def set_embedding(self, text_hash: str, embedding: Any) -> None:
        self.embedding_cache.set(f"emb:{text_hash}", embedding)

# Global cache manager instance
cache_manager = CacheManager()

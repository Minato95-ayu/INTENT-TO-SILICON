# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

"""
AAYU Runtime — Query Cache
Provides an LRU query result cache with TTL-based expiration
and automatic invalidation on write operations.
"""

import time
import threading
from collections import OrderedDict


class CacheEngine:
    """
    LRU query cache with TTL expiration for the AAYU database subsystem.

    Features:
    - LRU eviction when max_size is reached
    - TTL-based expiration (default 60 seconds)
    - Thread-safe access via RLock
    - Automatic invalidation on table writes
    - Cache statistics for monitoring
    """

    def __init__(self, max_size=256, default_ttl=60):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.store = OrderedDict()  # key -> {"value": ..., "expires_at": ...}
        self._lock = threading.RLock()
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "invalidations": 0,
        }

    def get(self, key):
        """
        Retrieve a cached value by key.

        Returns None if key is not found or has expired.
        Moves accessed items to the end (most recently used).
        """
        with self._lock:
            if key not in self.store:
                self._stats["misses"] += 1
                return None

            entry = self.store[key]

            # Check TTL expiration
            if entry["expires_at"] < time.monotonic():
                del self.store[key]
                self._stats["misses"] += 1
                return None

            # Move to end (most recently used)
            self.store.move_to_end(key)
            self._stats["hits"] += 1
            return entry["value"]

    def put(self, key, value, ttl=None):
        """
        Store a value in the cache.

        Args:
            key: Cache key (typically a SQL query string + params hash).
            value: Query result to cache.
            ttl: Time-to-live in seconds (uses default_ttl if not specified).
        """
        ttl = ttl if ttl is not None else self.default_ttl

        with self._lock:
            # If key exists, update it
            if key in self.store:
                self.store.move_to_end(key)

            self.store[key] = {
                "value": value,
                "expires_at": time.monotonic() + ttl,
            }

            # Evict oldest entries if over max_size
            while len(self.store) > self.max_size:
                self.store.popitem(last=False)
                self._stats["evictions"] += 1

    def invalidate_table(self, table_name):
        """
        Invalidate all cache entries related to a specific table.

        Called automatically when a write operation (INSERT, UPDATE, DELETE)
        is performed on the table.

        Args:
            table_name: Name of the table that was modified.
        """
        with self._lock:
            keys_to_remove = [
                key for key in self.store
                if table_name.lower() in key.lower()
            ]
            for key in keys_to_remove:
                del self.store[key]
                self._stats["invalidations"] += 1

    def clear(self):
        """Clear all cached entries."""
        with self._lock:
            self.store.clear()

    def stats(self):
        """
        Return cache performance statistics.

        Returns:
            dict: Contains hits, misses, evictions, invalidations,
                  size, hit_rate.
        """
        with self._lock:
            total = self._stats["hits"] + self._stats["misses"]
            return {
                **self._stats,
                "size": len(self.store),
                "max_size": self.max_size,
                "hit_rate": (self._stats["hits"] / total * 100) if total > 0 else 0.0,
            }

    def cleanup_expired(self):
        """Remove all expired entries from the cache."""
        now = time.monotonic()
        with self._lock:
            expired_keys = [
                key for key, entry in self.store.items()
                if entry["expires_at"] < now
            ]
            for key in expired_keys:
                del self.store[key]
            return len(expired_keys)

from django.core.cache import cache

def get_cached(key):
    return cache.get(key)

def set_cached(key, value, ttl=None):
    cache.set(key, value, timeout=ttl)

def delete_cached(key):
    cache.delete(key)

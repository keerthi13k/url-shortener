import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

CACHE_EXPIRY = 3600

def get_cached_url(short_code: str):
    return redis_client.get(f"url:{short_code}")

def set_cached_url(short_code: str, original_url: str):
    redis_client.setex(f"url:{short_code}", CACHE_EXPIRY, original_url)

def delete_cached_url(short_code: str):
    redis_client.delete(f"url:{short_code}")

def increment_click_cache(short_code: str):
    redis_client.incr(f"clicks:{short_code}")

def get_cached_clicks(short_code: str):
    clicks = redis_client.get(f"clicks:{short_code}")
    return int(clicks) if clicks else 0
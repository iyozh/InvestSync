import json

import redis
from app.src.core.config import settings


class RedisService:
    def __init__(self):
        self.client = redis.Redis(host=settings.REDIS_HOST)

    def set_key(self, key, value, expiration_time):
        self.client.set(key, json.dumps(value), ex=expiration_time)

    def get_cached_value(self, key):
        cached_value = self.client.get(key)
        return json.loads(cached_value) if cached_value else None

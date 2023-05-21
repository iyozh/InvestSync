import json

import redis.asyncio as redis
from app.src.core.config import settings


class RedisService:
    def __init__(self):
        self.client = redis.Redis(host=settings.REDIS_HOST)

    async def set_key(self, key, value, expiration_time):
        await self.client.set(key, json.dumps(value), ex=expiration_time)

    async def get_cached_value(self, key):
        cached_value = await self.client.get(key)
        return json.loads(cached_value) if cached_value else None

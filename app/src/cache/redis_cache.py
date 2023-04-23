import redis
from app.src.core.config import settings

redis_client = redis.Redis(host=settings.REDIS_HOST)

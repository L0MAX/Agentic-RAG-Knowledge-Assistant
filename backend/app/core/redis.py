from redis import Redis

from app.core.config import get_settings


def get_redis() -> Redis:
    """Return a Redis client from configured REDIS_URL. Callers own connection lifetime."""
    return Redis.from_url(get_settings().redis_url, decode_responses=True)

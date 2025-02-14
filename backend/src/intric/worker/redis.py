import redis.asyncio as aioredis

from intric.main.config import SETTINGS

pool = aioredis.ConnectionPool.from_url(
    f"redis://{SETTINGS.redis_host}:{SETTINGS.redis_port}"
)
r = aioredis.Redis(connection_pool=pool)

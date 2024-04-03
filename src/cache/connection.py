from typing import Optional

from redis.asyncio import ConnectionPool

from core.config import CacheConfig


class RedisConnection:
    def __init__(self):
        self.pool: Optional[ConnectionPool] = None

    def init(self, config: CacheConfig):
        self.pool = ConnectionPool(**config.model_dump())

    def close(self):
        if self.pool:
            self.pool.close()
            self.pool = None


redis_pool = RedisConnection()

import asyncio

import asyncpg
import redis.asyncio as aioredis

from .env import Env


class DBService:
    pool: asyncpg.Pool = None
    redis: aioredis.Redis = None

    @classmethod
    async def init(cls):
        cls.pool = await asyncpg.create_pool(Env.get("dsn"))
        pool = aioredis.ConnectionPool.from_url(Env.get("redis_url"))
        cls.redis = aioredis.Redis.from_pool(pool)

    @classmethod
    async def close(cls):
        async with asyncio.timeout(10):
            await cls.pool.close()
            await cls.redis.aclose(True)

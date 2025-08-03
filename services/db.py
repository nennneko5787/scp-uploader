import asyncpg

from .env import Env

class DBService:
    pool: asyncpg.Pool = None
    
    @classmethod
    async def init(cls):
        cls.pool = await asyncpg.create_pool(Env.get("dsn"))
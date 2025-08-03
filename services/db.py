import os

import asyncpg
import dotenv

dotenv.load_dotenv()

class DBService:
    pool: asyncpg.Pool = None
    
    @classmethod
    async def init(cls):
        cls.pool = await asyncpg.create_pool(os.getenv("dsn"))
from fastapi import Cookie, HTTPException

from objects import User
from services.db import DBService


async def verifyUserNoneable(token: str = Cookie(None)):
    if not token:
        return

    userId = await DBService.redis.get(f"session:user:{token}")
    if not userId:
        raise HTTPException(401, detail="Login required")

    record = await DBService.pool.fetchrow(
        "SELECT * FROM users WHERE id = $1", str(userId, "utf-8")
    )

    return User.model_validate(dict(record))


async def verifyUser(token: str = Cookie(None)):
    if not token:
        raise HTTPException(401, detail="Login required")

    userId = await DBService.redis.get(f"session:user:{token}")
    if not userId:
        raise HTTPException(401, detail="Login required")

    record = await DBService.pool.fetchrow(
        "SELECT * FROM users WHERE id = $1", str(userId, "utf-8")
    )

    return User.model_validate(dict(record))

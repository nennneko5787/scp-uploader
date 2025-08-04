import secrets

from fastapi import APIRouter, Cookie, HTTPException, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from objects import ServiceUserProfile
from services.db import DBService

router = APIRouter()


class LoginRequest(BaseModel):
    authCode: str = Field(min_length=6, max_length=6, pattern=r"[a-zA-Z0-9]{6}")


@router.get("/logout")
async def logout(token: str = Cookie(None)):
    if not token:
        raise HTTPException(401, detail="Login required")

    userId = await DBService.redis.get(f"session:user:{token}")
    if not userId:
        raise HTTPException(401, detail="Login required")

    await DBService.redis.get(f"session:user:{token}")

    response = RedirectResponse("/")
    response.delete_cookie("token")
    return response


@router.post("/api/auth/login")
async def authLogin(
    model: LoginRequest,
    response: Response,
):
    """ログイン(登録も兼用)"""

    user = await DBService.redis.get(f"sonolus:reverseAuth:{model.authCode}")
    if not user:
        raise HTTPException(401, "Login failed")

    user = ServiceUserProfile.model_validate_json(str(user, encoding="utf-8"))

    row = await DBService.pool.fetchrow("SELECT * FROM users WHERE id = $1", user.id)

    if not row:
        # アカウントがない場合はユーザー作成
        await DBService.pool.execute(
            """
                INSERT INTO users (id, handle, name, about_me)
                VALUES ($1, $2, $3, $4)
            """,
            user.id,
            user.handle,
            user.name,
            user.aboutMe,
        )

    token = secrets.token_urlsafe(32)
    await DBService.redis.set(f"session:user:{token}", user.id, 60 * 60 * 24 * 365)
    response.set_cookie("token", token, max_age=60 * 60 * 24 * 365, httponly=True)

    await DBService.redis.delete(f"sonolus:reverseAuth:{model.authCode}")

    return {"detail": "logined"}

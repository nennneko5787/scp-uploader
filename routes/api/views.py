import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from services.db import DBService
from services.env import Env

router = APIRouter()


class AddViewRequest(BaseModel):
    gumimegu: str


@router.post("/api/mikurinlen/{fileId:str}")
async def adminPost(model: AddViewRequest, fileId: str):
    response = await httpx.AsyncClient().post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        json={
            "secret": Env.get("turnstile_secret"),
            "response": model.gumimegu,
        },
    )
    jsonData = response.json()
    if not jsonData["success"]:
        return "NG"

    await DBService.pool.fetchrow(
        """
            UPDATE files
            SET views = views + 1
            WHERE id = $1
            RETURNING *
        """,
        fileId,
    )

    return "OK"

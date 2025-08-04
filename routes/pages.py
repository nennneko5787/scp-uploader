import html
from typing import get_args

import httpx
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
)
from fastapi.templating import Jinja2Templates

from objects import Localization, User
from services.auth import verifyUser, verifyUserNoneable
from services.db import DBService
from services.files import fetchUser

router = APIRouter()
templates = Jinja2Templates("pages")


def truncateTo2Decimal(value):
    return int(value * 100) / 100


templates.env.filters["truncate2"] = truncateTo2Decimal


@router.get("/")
def index(
    request: Request,
    response: Response,
    localization: str = Cookie("ja"),
    user: User = Depends(verifyUserNoneable),
):
    if localization not in get_args(Localization):
        localization = "ja"
        response.delete_cookie("localization")

    return templates.TemplateResponse(
        request, f"{localization}/index.html", {"user": user}
    )


@router.get("/users/{userId:str}")
async def user(
    request: Request,
    response: Response,
    userId: str,
    localization: str = Cookie("ja"),
    user: User = Depends(verifyUserNoneable),
):
    targetUser = User.model_validate(await fetchUser(userId))

    if localization not in get_args(Localization):
        localization = "ja"
        response.delete_cookie("localization")

    return templates.TemplateResponse(
        request, f"{localization}/user.html", {"user": user, "targetUser": targetUser}
    )


@router.get("/files/{fileId:str}")
async def file(
    request: Request,
    response: Response,
    fileId: str,
    localization: str = Cookie("ja"),
    user: User = Depends(verifyUserNoneable),
):
    file = await get(fileId)
    file.description = html.escape(file.description)

    if localization not in get_args(Localization):
        localization = "ja"
        response.delete_cookie("localization")

    return templates.TemplateResponse(
        request, f"{localization}/file.html", {"user": user, "file": file}
    )


@router.get("/files/{fileId:str}/download")
async def download(
    backgroundTask: BackgroundTasks,
    fileId: str,
):
    file = await get(fileId)

    async def background():
        await DBService.pool.fetchrow(
            """
                UPDATE files
                SET downloads = downloads + 1
                WHERE id = $1
                RETURNING *
            """,
            file.id,
        )

    backgroundTask.add_task(background)

    async with httpx.AsyncClient() as http:
        response = await http.get(
            f"https://r2.scp-uploader.f5.si/{file.author.id}/{file.id}.scp"
        )
        return Response(
            response.content,
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{file.id}.scp"'},
        )


@router.get("/files/{fileId:str}/edit")
async def edit(
    request: Request,
    response: Response,
    fileId: str,
    localization: str = Cookie("ja"),
    user: User = Depends(verifyUserNoneable),
):
    file = await get(fileId)

    if localization not in get_args(Localization):
        localization = "ja"
        response.delete_cookie("localization")

    if user.id != file.author.id:
        raise HTTPException(403, "Forbidden")

    return templates.TemplateResponse(
        request, f"{localization}/edit.html", {"user": user, "file": file}
    )


@router.get("/login")
def login(
    request: Request,
    response: Response,
    localization: str = Cookie("ja"),
    user: User = Depends(verifyUserNoneable),
):
    if localization not in get_args(Localization):
        localization = "ja"
        response.delete_cookie("localization")

    return templates.TemplateResponse(
        request, f"{localization}/login.html", {"user": user}
    )


@router.get("/upload")
def upload(
    request: Request,
    response: Response,
    localization: str = Cookie("ja"),
    user: User = Depends(verifyUser),
):
    if localization not in get_args(Localization):
        localization = "ja"
        response.delete_cookie("localization")

    return templates.TemplateResponse(
        request, f"{localization}/upload.html", {"user": user}
    )

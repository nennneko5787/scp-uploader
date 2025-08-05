from typing import List, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from objects import User
from services.auth import verifyUser
from services.files import (
    delete,
    edit,
    get,
    getFilesByDownloads,
    getFilesByNewer,
    getFilesByViews,
)

router = APIRouter()


@router.get("/api/files")
async def files(
    page: int = Query(1, ge=1), type: Literal["new", "views", "downloads"] = "new"
):
    match type:
        case "new":
            func = getFilesByNewer
        case "views":
            func = getFilesByViews
        case "downloads":
            func = getFilesByDownloads

    files = await func(page=page)
    return files


class EditRequest(BaseModel):
    name: str
    description: str
    tags: List[str]
    public: bool


@router.patch("/api/files/{fileId:str}/edit")
async def editFile(model: EditRequest, fileId: str, user: User = Depends(verifyUser)):
    file = await get(fileId)

    if user.id != file.author.id:
        raise HTTPException(403, "Forbidden")

    await edit(file.id, model.name, model.description, model.tags, model.public)


@router.delete("/api/files/{fileId:str}")
async def deleteFile(fileId: str, user: User = Depends(verifyUser)):
    file = await get(fileId)

    if user.id != file.author.id:
        raise HTTPException(403, "Forbidden")

    await delete(file)

import asyncio
import json
import uuid
import zipfile
from io import BytesIO

import aioboto3
import httpx
from fastapi import APIRouter, Depends, Form, HTTPException, Response, UploadFile
from fastapi import File as FileFunc

from objects import File, User
from services.auth import verifyUser
from services.db import DBService
from services.env import Env

router = APIRouter()


MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post("/api/upload")
async def upload(
    response: Response,
    name: str = Form(),
    description: str = Form(),
    tags: str = Form(),
    public: bool = Form(),
    mikulen: str = Form(),
    file: UploadFile = FileFunc(),
    user: User = Depends(verifyUser),
):
    response.status_code = 201

    tsres = await httpx.AsyncClient().post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        json={
            "secret": Env.get("ts_secret"),
            "response": mikulen,
        },
    )
    jsonData = tsres.json()
    if not jsonData["success"]:
        raise HTTPException(400, "Failed to solve CAPTCHA")

    if file.size >= MAX_FILE_SIZE:
        raise HTTPException(413, "Files must not exceed 20MB.")

    if not file.filename.endswith(".scp"):
        raise HTTPException(
            400, "The file extension of the uploaded file must be .scp."
        )

    if len(name) > 60:
        raise HTTPException(413, "Name must not exceed 60 characters.")

    if len(description) > 600:
        raise HTTPException(413, "Name must not exceed 600 characters.")

    tags = json.loads(tags)

    if not isinstance(tags, list):
        raise HTTPException(400, "Tags ???")

    for tag in tags:
        if len(tag) > 60:
            raise HTTPException(413, "Tag must not exceed 60 characters.")

    fileContent = BytesIO(await file.read())
    title = await asyncio.to_thread(zipProcess, fileContent)

    fileId = uuid.uuid4()

    session = aioboto3.Session()

    async with session.client(
        service_name="s3",
        endpoint_url=Env.get("s3_endpoint"),
        aws_access_key_id=Env.get("s3_access_key_id"),
        aws_secret_access_key=Env.get("s3_secret_access_key"),
        region_name="auto",
    ) as client:
        await client.upload_fileobj(
            fileContent, Env.get("s3_bucket"), f"{user.id}/{str(fileId)}.scp"
        )

    row = dict(
        await DBService.pool.fetchrow(
            """
                INSERT INTO files (id, author_id, name, description, tags, title, size, public)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING *
            """,
            fileId,
            user.id,
            name,
            description,
            tags,
            title,
            file.size / (1024 * 1024),
            public,
        )
    )
    row["author"] = user.model_dump(by_alias=True)
    del row["author_id"]

    return File.model_validate(row)


def zipProcess(fileContent: BytesIO) -> str:
    with zipfile.ZipFile(fileContent) as zipFile:
        fileList = zipFile.namelist()
        fileSet = set(fileList)

        # 必須ファイル確認
        if "sonolus/package" not in fileSet or "sonolus/info" not in fileSet:
            raise HTTPException(
                400, "Broken scp file (missing sonolus/package or sonolus/info)"
            )

        with zipFile.open("sonolus/info") as infoFile:
            infoJson = json.load(infoFile)

        buttons = infoJson.get("buttons", [])
        missingFolders = []
        incompleteFolders = []

        for button in buttons:
            folderType = button.get("type", "") + "s"  # 例: "stage" -> "stages"

            if folderType == "configurations":
                continue

            folderPath = f"sonolus/{folderType}/"  # 例: "sonolus/stages/"

            folderExists = any(name.startswith(folderPath) for name in fileList)

            if folderExists:
                expectedListFile = folderPath + "list"
                expectedInfoFile = folderPath + "info"

                if expectedListFile not in fileSet or expectedInfoFile not in fileSet:
                    incompleteFolders.append(folderPath)
            else:
                missingFolders.append(folderPath)

        if not missingFolders and not incompleteFolders:
            return infoJson.get("title", "unknown")
        else:
            raise HTTPException(
                400,
                f"Broken scp file: missing folders = {missingFolders}, incomplete folders = {incompleteFolders}",
            )

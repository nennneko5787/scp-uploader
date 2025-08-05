from typing import List

import aioboto3

from objects import File, User

from .db import DBService
from .env import Env


async def fetchUser(userId: int):
    return dict(
        await DBService.pool.fetchrow("SELECT * FROM users WHERE id = $1", userId)
    )


async def get(id: int):
    row = await DBService.pool.fetchrow("SELECT * FROM files WHERE id = $1", id)

    if not row:
        raise Exception("File not found.")
    row = dict(row)

    row["author"] = await fetchUser(row["author_id"])
    del row["author_id"]

    return File.model_validate(row)


async def getUserFilesByNewer(*, user: User, page: int):
    perPage = 10
    rows = await DBService.pool.fetch(
        "SELECT * FROM files WHERE author_id = $3 ORDER BY created_at DESC LIMIT $1 OFFSET ($2 - 1) * $1",
        perPage,
        page,
        user.id,
    )
    files: List[File] = []

    for row in rows:
        row = dict(row)
        row["author"] = user
        del row["author_id"]

        file = File.model_validate(row)
        files.append(file)

    return files


async def getFilesByQueries(*, query: str, page: int):
    perPage = 10
    rows = await DBService.pool.fetch(
        "SELECT * FROM files WHERE public = true AND name ILIKE $3 ORDER BY created_at DESC LIMIT $1 OFFSET ($2 - 1) * $1",
        perPage,
        page,
        f"%{query}%",
    )
    files: List[File] = []

    for row in rows:
        row = dict(row)
        row["author"] = await fetchUser(row["author_id"])
        del row["author_id"]

        file = File.model_validate(row)
        files.append(file)

    return files


async def getFilesByNewer(*, page: int):
    perPage = 10
    rows = await DBService.pool.fetch(
        "SELECT * FROM files WHERE public = true ORDER BY created_at DESC LIMIT $1 OFFSET ($2 - 1) * $1",
        perPage,
        page,
    )
    files: List[File] = []

    for row in rows:
        row = dict(row)
        row["author"] = await fetchUser(row["author_id"])
        del row["author_id"]

        file = File.model_validate(row)
        files.append(file)

    return files


async def getFilesByViews(*, page: int):
    perPage = 10
    rows = await DBService.pool.fetch(
        "SELECT * FROM files WHERE public = true ORDER BY views ASC LIMIT $1 OFFSET ($2 - 1) * $1",
        perPage,
        page,
    )
    files: List[File] = []

    for row in rows:
        row = dict(row)
        row["author"] = await fetchUser(row["author_id"])
        del row["author_id"]

        file = File.model_validate(row)
        files.append(file)

    return files


async def getFilesByDownloads(*, page: int):
    perPage = 10
    rows = await DBService.pool.fetch(
        "SELECT * FROM files WHERE public = true ORDER BY downloads ASC LIMIT $1 OFFSET ($2 - 1) * $1",
        perPage,
        page,
    )
    files: List[File] = []

    for row in rows:
        row = dict(row)
        row["author"] = await fetchUser(row["author_id"])
        del row["author_id"]

        file = File.model_validate(row)
        files.append(file)

    return files


async def edit(fileId: str, name: str, description: str, tags: List[str], public: bool):
    row = dict(
        await DBService.pool.fetchrow(
            """
                UPDATE files
                    SET
                    name          = $2,
                    tags          = $3,
                    description   = $4,
                    public        = $5,
                    edited_at     = now()
                WHERE id = $1
                RETURNING *
            """,
            fileId,
            name,
            tags,
            description,
            public,
        )
    )
    row["author"] = await fetchUser(row["author_id"])
    del row["author_id"]

    article = File.model_validate(row)

    return article


async def delete(file: File):
    session = aioboto3.Session()
    async with session.client(
        service_name="s3",
        endpoint_url=Env.get("s3_endpoint"),
        aws_access_key_id=Env.get("s3_access_key_id"),
        aws_secret_access_key=Env.get("s3_secret_access_key"),
        region_name="auto",
    ) as client:
        await client.delete_object(
            Bucket=Env.get("s3_bucket"), Key=f"{file.author.id}/{file.id}.scp"
        )
    await DBService.pool.execute("DELETE FROM files WHERE id = $1", file.id)

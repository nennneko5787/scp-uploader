from typing import List

from objects import File

from .db import DBService


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


async def getFilesByNewer(*, page: int):
    perPage = 10
    rows = await DBService.pool.fetch(
        "SELECT * FROM files ORDER BY created_at DESC LIMIT $1 OFFSET ($2 - 1) * $1",
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
        "SELECT * FROM files ORDER BY views ASC LIMIT $1 OFFSET ($2 - 1) * $1",
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
        "SELECT * FROM files ORDER BY downloads ASC LIMIT $1 OFFSET ($2 - 1) * $1",
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


async def edit(
    articleId: int,
    name: str,
    description: str,
    tags: List[str],
):
    row = dict(
        await DBService.pool.fetchrow(
            """
                UPDATE files
                    SET
                    name          = $2,
                    tags          = $3,
                    description   = $4,
                    edited_at     = now()
                WHERE id = $1
                RETURNING *
            """,
            articleId,
            name,
            tags,
            description,
        )
    )
    row["author"] = await fetchUser(row["author_id"])
    del row["author_id"]

    article = File.model_validate(row)

    return article

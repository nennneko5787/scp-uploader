from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Query,
    Request,
    Response,
)
from fastapi.templating import Jinja2Templates

from objects import User, localizations
from services.auth import verifyUserNoneable
from services.files import getFilesByQueries

router = APIRouter()
templates = Jinja2Templates("pages")


def truncateTo2Decimal(value):
    return int(value * 100) / 100


templates.env.filters["truncate2"] = truncateTo2Decimal


@router.get("/search")
async def search(
    request: Request,
    response: Response,
    query: str = Query(""),
    page: int = Query(1, ge=1),
    localization: str = Cookie("ja"),
    user: User = Depends(verifyUserNoneable),
):
    if localization not in localizations:
        localization = "ja"
        response.delete_cookie("localization")

    files = []
    if query:
        files = await getFilesByQueries(query=query, page=page)

    return templates.TemplateResponse(
        request,
        f"{localization}/search.html",
        {"user": user, "files": files, "page": page, "query": query},
    )

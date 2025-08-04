from fastapi import APIRouter, Response

from objects import SRL, Localization, ServerInfo, ServerInfoButton
from services.i18n import I18n

router = APIRouter()


@router.get("/sonolus/info")
async def sonolusInfo(response: Response, localization: Localization) -> ServerInfo:
    response.headers.update({"Sonolus-Version": "1.0.0"})
    return ServerInfo(
        title=I18n.get("server.info.title", localization),
        description=I18n.get("server.info.description", localization),
        buttons=[ServerInfoButton(type="authentication")],
        configuration={"options": []},
        banner=SRL(hash=None, url=None),
    )

from fastapi import APIRouter, Header, Response

from objects import SRL, Localization, ServerInfo, ServerInfoButton, ServiceUserProfile
from services.db import DBService
from services.i18n import I18n

router = APIRouter()


@router.get("/sonolus/info")
async def sonolusInfo(
    response: Response,
    localization: Localization,
    token: str = Header(None, alias="Sonolus-Session"),
) -> ServerInfo:
    response.headers.update({"Sonolus-Version": "1.0.0"})

    description = I18n.get("server.info.description", localization)
    if token:
        user = await DBService.redis.get(f"sonolus:user:{token}")
        authCode = await DBService.redis.get(f"sonolus:authCode:{token}")

        if user:
            user = ServiceUserProfile.model_validate_json(str(user, "utf-8"))
            description += "\n" + I18n.get(
                "server.info.nowLogined",
                localization,
                name=f"{user.name}#{user.handle}",
            )

        if authCode:
            authCode = str(authCode, "utf-8")
            description += "\n\n" + I18n.get(
                "server.info.yourAuthCode", localization, authCode=authCode
            )

    return ServerInfo(
        title=I18n.get("server.info.title", localization),
        description=description,
        buttons=[ServerInfoButton(type="authentication")],
        configuration={"options": []},
        banner=SRL(hash=None, url=None),
    )

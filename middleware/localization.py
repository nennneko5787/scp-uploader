from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse


class LocalizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cookieName = "localization"

        if cookieName in request.cookies:
            return await call_next(request)

        acceptLang = request.headers.get("accept-language", "").lower()
        if acceptLang == "":
            return await call_next(request)

        lang = "ja" if acceptLang.startswith("ja") else "en"

        response = RedirectResponse(url=str(request.url))
        response.set_cookie(
            key=cookieName,
            value=lang,
            max_age=60 * 60 * 24 * 365,
            httponly=False,
            samesite="lax",
        )
        return response

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from middleware.localization import LocalizationMiddleware
from routes import pages, search
from routes.api import auth, files, upload, views
from routes.sonolus import auth as sonolusAuth
from routes.sonolus import info as sonolusInfo
from services.db import DBService


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DBService.init()
    yield
    await DBService.close()


app = FastAPI(
    lifespan=lifespan,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    swagger_ui_oauth2_redirect_url=None,
)

app.mount("/static", StaticFiles(directory="static"), "static")

app.add_middleware(LocalizationMiddleware)

app.include_router(sonolusInfo.router)
app.include_router(sonolusAuth.router)
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(files.router)
app.include_router(upload.router)
app.include_router(views.router)
app.include_router(search.router)


@app.get("/favicon.ico")
def faviconIco():
    return FileResponse("favicon.ico")

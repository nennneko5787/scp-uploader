from contextlib import asynccontextmanager

from fastapi import FastAPI

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

app.include_router(sonolusInfo.router)
app.include_router(sonolusAuth.router)

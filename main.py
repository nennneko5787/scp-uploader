from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.db import DBService

@asynccontextmanager
async def lifespan(app: FastAPI):
    await DBService.init()
    yield
    await DBService.close()

app = FastAPI(lifespan=lifespan)

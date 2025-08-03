from fastapi import FastAPI

from routes import neta

app = FastAPI()

app.include_router(neta.router)
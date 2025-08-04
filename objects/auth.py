from pydantic import BaseModel

from .user import ServiceUserProfile


class ServerAuthenticateRequest(BaseModel):
    type: str
    address: str
    time: int
    userProfile: ServiceUserProfile


class ServerAuthenticateResponse(BaseModel):
    session: str
    expiration: int

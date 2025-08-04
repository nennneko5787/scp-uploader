from typing import List

from pydantic import BaseModel


class ServiceUserProfile(BaseModel):
    id: str
    handle: str
    name: str
    avatarType: str
    avatarForegroundType: str
    avatarForegroundColor: str
    avatarBackgroundType: str
    avatarBackgroundColor: str
    bannerType: str
    aboutMe: str
    favorites: List[str]

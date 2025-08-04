from datetime import datetime, timedelta, timezone
from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_snake

from .user import User


class File(BaseModel):
    id: UUID4
    createdAt: datetime
    editedAt: Optional[datetime]
    author: User
    name: str
    description: str
    tags: List[str]
    title: str
    size: float
    views: int
    downloads: int

    @field_validator("createdAt", mode="before")
    @classmethod
    def convertCreatedAt(cls, v: datetime) -> datetime:
        return v.astimezone(timezone(timedelta(hours=9)))

    @field_validator("editedAt", mode="before")
    @classmethod
    def convertEditedAt(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None:
            return v.astimezone(timezone(timedelta(hours=9)))
        return v

    model_config = ConfigDict(alias_generator=to_snake)

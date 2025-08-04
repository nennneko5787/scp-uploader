from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_snake


class User(BaseModel):
    id: str
    handle: str
    name: str
    aboutMe: str

    model_config = ConfigDict(alias_generator=to_snake)

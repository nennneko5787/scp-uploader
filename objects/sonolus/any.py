from typing import List, Literal, Optional

from pydantic import BaseModel

type Localization = Literal[
    "el", "en", "es", "fr", "id", "it", "ja", "ko", "ru", "tr", "zhs", "zht"
]
localizations: List[Localization] = [
    "el",
    "en",
    "es",
    "fr",
    "id",
    "it",
    "ja",
    "ko",
    "ru",
    "tr",
    "zhs",
    "zht",
]


class SRL(BaseModel):
    hash: Optional[str]
    url: Optional[str]

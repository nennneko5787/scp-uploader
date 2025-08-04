from typing import Dict, List, Literal, Optional

from pydantic import BaseModel

from .any import SRL


class ServerInfoButton(BaseModel):
    type: Literal[
        "authentication",
        "multiplayer",
        "post",
        "playlist",
        "level",
        "replay",
        "skin",
        "background",
        "effect",
        "particle",
        "engine",
        "configuration",
    ]


class ServerInfo(BaseModel):
    title: str
    description: Optional[str]
    buttons: List[ServerInfoButton]
    configuration: Dict[str, List[Dict[str, str]]]
    banner: Optional[SRL]

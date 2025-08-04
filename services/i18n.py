import json
from typing import Dict

from objects import Localization


class I18n:
    i18nTable: Dict[str, Dict[Localization, str]] = {}

    with open("i18n.json", "r", encoding="utf-8") as f:
        i18nTable = json.load(f)

    @classmethod
    def get(cls, key: str, localization: Localization, *args, **kwargs) -> str:
        langs = cls.i18nTable.get(key, None)

        if not langs:
            raise ValueError(f'I18n table "{key}" is not found.')

        default = langs.get("en", None)

        if not default:
            raise ValueError(
                f'I18n table "{key}" is not found (Because default locale is not set).'
            )

        return langs.get(localization, default).format(*args, **kwargs)

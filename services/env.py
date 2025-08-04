import os

import dotenv

dotenv.load_dotenv()


class Env:
    @classmethod
    def get(cls, key: str) -> str:
        value = os.getenv(key)

        if not value:
            raise ValueError(f'Environ "{key}" is not found.')

        return value

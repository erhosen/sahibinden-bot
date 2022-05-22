import random
from typing import Iterable, List

from pydantic import BaseSettings


class Settings(BaseSettings):
    SAHIBINDEN_TIMEOUT: int = 10
    PROXIES: List[str]

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_BUCKET_NAME: str

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHANNEL_ID: int

    SENTRY_DSN: str

    @property
    def httpx_proxies(self) -> Iterable[dict]:
        shuffled_proxies = list(self.PROXIES)
        random.shuffle(shuffled_proxies)
        for proxy in shuffled_proxies:
            yield {"http://": proxy, "https://": proxy}

    class Config:
        env_file = ".env"


settings = Settings()

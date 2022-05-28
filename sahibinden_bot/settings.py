import random
from typing import Iterable, List

from pydantic import BaseSettings


class Settings(BaseSettings):
    SAHIBINDEN_TIMEOUT: int = 10
    PROXIES: List[str]

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_BUCKET_NAME: str
    AWS_ENDPOINT_URL: str

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHANNEL_ID: int

    SENTRY_DSN: str

    @property
    def httpx_proxies(self) -> Iterable[dict]:
        shuffled_proxies = list(self.PROXIES)
        random.shuffle(shuffled_proxies)
        for proxy in shuffled_proxies:
            yield {"http://": proxy, "https://": proxy}

    @property
    def s3_credentials(self) -> dict:
        return {
            "bucket_name": self.AWS_BUCKET_NAME,
            "endpoint_url": self.AWS_ENDPOINT_URL,
            "aws_access_key_id": self.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": self.AWS_SECRET_ACCESS_KEY,
        }

    class Config:
        env_file = ".env"


settings = Settings()

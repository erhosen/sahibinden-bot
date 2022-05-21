from pydantic import BaseSettings


class Settings(BaseSettings):
    SAHIBINDEN_COOKIE: str

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_BUCKET_NAME: str

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHANNEL_ID: int

    SENTRY_DSN: str

    class Config:
        env_file = ".env"


settings = Settings()

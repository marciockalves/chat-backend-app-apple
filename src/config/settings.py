from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "Chat NAtive API"
    DEBUG: bool = True


    POSTGRES_USER: str = "chat_admin"
    POSTGRES_PASSWORD: str = "chat_password_2026"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432   
    POSTGRES_DB: str = "chat_db"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    @property
    def database_url(self)-> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra = "ignore"
    )

settings= Settings()
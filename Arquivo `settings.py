from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")

settings = Settings()

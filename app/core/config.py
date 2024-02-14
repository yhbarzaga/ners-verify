from functools import lru_cache
from typing import Optional, List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "NERS"
    sqlalchemy_database_uri: Optional[str]
    backend_cors_origins: List[AnyHttpUrl] = []


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()

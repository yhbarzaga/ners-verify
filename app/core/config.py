from functools import lru_cache
from typing import Optional, List

from pydantic.v1 import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    project_name: str = "NERS"
    sqlalchemy_database_uri: Optional[str]
    backend_cors_origins: List[AnyHttpUrl] = []

    # verify provider
    verify_base_url: str
    verify_client_id: str
    verify_client_secret: str
    verify_api_key: str
    verify_user_name: str


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()

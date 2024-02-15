from pydantic_settings import BaseSettings

from app.core.config import get_settings

settings = get_settings()


class VerifySettings(BaseSettings):
    """Verify settings."""

    api_base_url: str = settings.verify_base_url
    client_id: str = settings.verify_client_id
    client_secret: str = settings.verify_client_secret
    api_key: str = settings.verify_api_key
    user_name: str = settings.verify_user_name

    class Config:
        """load config from .env file"""

        env_prefix = "verify_"

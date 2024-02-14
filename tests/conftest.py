import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def fastapi_app():
    """Return FastApi app instance."""
    from app.main import app

    return app


@pytest.fixture(scope="session")
def client(fastapi_app) -> TestClient:
    """Main test client"""

    return TestClient(fastapi_app, base_url="http://ners.com")

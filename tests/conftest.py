import asyncio
from typing import Generator
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.db.base_class import Base
from app.db.session import engine
from app.services.ocr_processing.providers import VerifyProvider, get_ocr_provider
from tests.factories import StaffFactory, DocumentFactory


@pytest.fixture(scope="session")
def fastapi_app():
    """Return FastApi app instance."""
    from app.main import app

    return app


@pytest.fixture(scope="session")
def client(fastapi_app) -> TestClient:
    """Main test client"""

    return TestClient(
        fastapi_app,
        base_url="http://ners.com",
        backend_options={"loop_factory": asyncio.new_event_loop},
    )


@pytest.fixture
def ocr_provider_settings(mocker):
    """Mock OCR provider settings."""

    mocked = mocker.patch(
        "app.services.ocr_processing.providers._get_ocr_provider_settings",
        return_value=mock.Mock(),
        autospec=True,
    )

    yield mocked


def setup_db(connection):
    """Initialize database before executing tests"""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = SessionLocal(bind=connection)
    session.commit()
    session.close()


@pytest.fixture(scope="session")
def connection() -> Generator:
    """Connection object shared by all tests."""
    connection = engine.connect()  # type:ignore[attr-defined]
    setup_db(connection)
    yield connection
    connection.close()


@pytest.fixture(scope="session")
def db(connection: Generator) -> Generator:
    transaction = connection.begin()  # type:ignore[attr-defined]
    session = SessionLocal()

    StaffFactory._meta.sqlalchemy_session = session
    DocumentFactory._meta.sqlalchemy_session = session
    yield session

    session.close()
    transaction.rollback()


@pytest.fixture()
def seed_staff(db):
    """Fixture to seed staff."""

    def _create_object(**kwargs):
        staff = StaffFactory.create(**kwargs)
        db.commit()  # type:ignore[attr-defined]
        return staff

    return _create_object


@pytest.fixture()
def seed_document(db):
    """Fixture to seed document."""

    def _create_object(**kwargs):
        document = DocumentFactory.create(**kwargs)
        db.commit()  # type:ignore[attr-defined]
        return document

    return _create_object


@pytest.fixture
def mock_ocr_provider(fastapi_app):
    """Mock OCR provider to test service composition."""

    _ocr_provider = VerifyProvider(
        settings=mock.Mock(
            api_base_url="https://verify.api.com",
            client_id="my_client_id",
            client_secret="my_client_secret",
            api_key="my_api_key",
            user_name="my_user_name",
        )
    )
    _ocr_provider.get_document = mock.Mock()
    _ocr_provider.process_document = mock.Mock()
    _ocr_provider.post = mock.Mock()
    _ocr_provider.get = mock.Mock()

    fastapi_app.dependency_overrides[get_ocr_provider] = lambda: _ocr_provider

    yield _ocr_provider

    fastapi_app.dependency_overrides = {}

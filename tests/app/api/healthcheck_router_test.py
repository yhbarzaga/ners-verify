from fastapi.testclient import TestClient
from fastapi import status


def test_get_healthcheck_service_not_available(client: TestClient):
    response = client.get("/api/v1/health-check")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

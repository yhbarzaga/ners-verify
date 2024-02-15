import uuid

from fastapi.testclient import TestClient
from fastapi import status

from app.services.ocr_processing import DocumentFromProvider


class TestDocumentRouter:
    """Tests related to document endpoints"""

    def test_process_document_not_found(self, client: TestClient):
        """Test that when process document if staff id provided doesn't exist a NotFound is returned."""
        fake_id = str(uuid.uuid4())
        payload = {
            "file_url": "https://myurl.com",
            "file_name": "myFileName",
            "country": "US",
            "staff_id": fake_id,
        }

        response = client.post("api/v1/documents/", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == f"Internal user with id {fake_id} not found"

    def test_process_document_success(
        self,
        client: TestClient,
        seed_staff,
        mock_ocr_provider,
    ):
        """Test success process document."""
        mock_ocr_provider.process_document.return_value = DocumentFromProvider(
            id=99, total=101, name="Verify", provider_id=1
        )

        staff = seed_staff()
        payload = {
            "file_url": "https://myurl.com",
            "file_name": "myFileName",
            "country": "US",
            "staff_id": str(staff.internal_id),
        }

        response = client.post("api/v1/documents/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        mock_ocr_provider.process_document.assert_called()

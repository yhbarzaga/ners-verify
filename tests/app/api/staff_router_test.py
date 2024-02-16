import uuid
from fastapi.testclient import TestClient
from fastapi import status


class TestStaffRouter:
    """Tests related to staff endpoints"""

    def test_get_total_refund_unauthorized(self, client: TestClient):
        """Test that if API KEY is not provided forbidden access is returned."""

        response = client.get(
            f"api/v1/staff/{str(uuid.uuid4())}/refund",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_total_refund_not_found(self, client: TestClient):
        """Test get total with no valid id will return a not found."""
        fake_id = uuid.uuid4()

        response = client.get(
            f"api/v1/staff/{fake_id}/refund",
            headers={"Authorization": f"Bearer {str(uuid.uuid4())}"},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == f"Internal user with id {fake_id} not found"

    def test_get_total_refund(self, client: TestClient, seed_staff, seed_document):
        """Test success get total refund."""
        staff = seed_staff()
        _ = seed_document(staff_id=staff.uid)

        response = client.get(
            f"api/v1/staff/{str(staff.internal_id)}/refund",
            headers={"Authorization": f"Bearer {str(uuid.uuid4())}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() > 0

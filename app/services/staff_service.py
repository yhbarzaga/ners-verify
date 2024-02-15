from app.domain import StaffDomain
from app.exceptions import ResourceNotFound
from app.repositories import StaffRepository


class StaffService:
    """
    Staff service implementation.
    Use this class to place the business logic related to Staff
    """

    def __init__(
        self,
        repo: StaffRepository,
    ):
        """Initialize service."""

        self.repo = repo

    def get_by_internal_id(self, staff_id: str) -> StaffDomain:
        """Get the expected staff object from."""
        staff = self.repo.get_by_internal_id(staff_id)

        if staff is None:
            raise ResourceNotFound(f"Internal user with id {staff_id} not found")

        return staff

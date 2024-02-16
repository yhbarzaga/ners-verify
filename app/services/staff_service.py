import math

from app.domain import StaffDomain, StaffCreateDomain
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

    def get_by_internal_id(self, internal_id: str) -> StaffDomain:
        """Get the expected staff object from."""
        staff = self.repo.get_by_internal_id(internal_id)

        if staff is None:
            raise ResourceNotFound(f"Internal user with id {internal_id} not found")

        return staff

    def get_total(self, internal_id: str):
        """Get the total amount to be refund"""
        staff = self.get_by_internal_id(internal_id)
        total = sum(document.total for document in staff.documents)
        return math.ceil(total)

    def create(self, obj_in: StaffCreateDomain):
        """Create a new user"""
        return self.repo.create(obj_in)

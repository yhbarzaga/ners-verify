from typing import Optional

from app.domain.staff import (
    StaffDomain,
    StaffCreateDomain,
    StaffUpdateDomain,
)
from app.models import Staff
from app.repositories.base import BaseRepository


class StaffRepository(BaseRepository[Staff, StaffCreateDomain, StaffUpdateDomain]):
    """Staff repository implementation."""

    def get_by_internal_id(self, internal_id: str) -> Optional[StaffDomain]:
        staff = (
            self.session.query(Staff).filter(Staff.internal_id == internal_id).first()
        )

        return StaffDomain.from_orm(staff) if staff is not None else staff

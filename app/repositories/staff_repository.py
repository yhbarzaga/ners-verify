from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError

from app.domain.staff import (
    StaffDomain,
    StaffCreateDomain,
    StaffUpdateDomain,
)
from app.exceptions import CreationError
from app.models import Staff
from app.repositories.base import BaseRepository


class StaffRepository(BaseRepository[Staff, StaffCreateDomain, StaffUpdateDomain]):
    """Staff repository implementation."""

    def get_by_internal_id(self, internal_id: str) -> Optional[StaffDomain]:
        staff = (
            self.session.query(Staff).filter(Staff.internal_id == internal_id).first()
        )

        return StaffDomain.from_orm(staff) if staff is not None else staff

    def create(self, obj_in: StaffCreateDomain) -> StaffDomain:
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = Staff(**obj_in_data)
            self.session.add(db_obj)
            self.session.commit()
        except IntegrityError as err:
            self.session.rollback()
            raise CreationError(f"Error trying to create a user from staff, {err}")

        self.session.refresh(db_obj)

        return StaffDomain.from_orm(db_obj)

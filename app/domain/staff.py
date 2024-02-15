from uuid import UUID

from pydantic import BaseModel


class StaffAttrs(BaseModel):
    """Domain model definition for staff common attributes."""

    internal_id: str


class StaffCreateDomain(StaffAttrs):
    """Domain model definition for create a staff object"""


class StaffUpdateDomain(StaffAttrs):
    """Domain model definition for update a staff instance"""


class StaffDomain(StaffAttrs):
    """
    Domain model definition for staff object

    :note: class will act as a DTO, will be the object to communicate between service and data layer
    """

    uid: UUID

    class Config:
        from_attributes = True

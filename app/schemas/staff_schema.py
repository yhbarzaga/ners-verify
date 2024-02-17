from uuid import UUID

from pydantic.v1 import Field

from app.domain import StaffAttrs


class StaffCreateSchema(StaffAttrs):
    """Schema definition used to create."""


class StaffResponseSchema(StaffAttrs):
    """Response definition used to create."""

    uid: UUID = Field(exclude="Use this value whenever require staff_id")

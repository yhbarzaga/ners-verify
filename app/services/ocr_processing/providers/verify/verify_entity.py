from pydantic.v1 import BaseModel


class VerifyResponse(BaseModel):
    """Response schema definition to parse verify responses."""

    id: int
    total: float

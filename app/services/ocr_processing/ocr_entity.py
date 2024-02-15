from enum import IntEnum

from pydantic import BaseModel


class OCRProviderId(IntEnum):
    """Enum for OCR providers.

    <provider_name>: <id on table>
    """

    VERIFY = 1


class DocumentFromProvider(BaseModel):
    """Domain model definition for document data that comes from the OCR provider."""

    id: int
    total: float
    name: str
    provider_id: int


class DocumentAttrs(BaseModel):
    """Base class to hold common document attributes."""

    id: int = None
    total: float = None


class Document(DocumentAttrs, BaseModel):
    """Domain model definition for document information."""

    class Config:
        """Config metaclass."""

        orm_mode = True


class DocumentResponse(Document):
    """Response model definition for document information"""

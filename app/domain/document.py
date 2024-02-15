from uuid import UUID

from pydantic import BaseModel


class DocumentAttrs(BaseModel):
    """Domain model definition for document common attributes."""

    total: float
    staff_id: UUID


class DocumentCreateDomain(DocumentAttrs):
    """Domain model definition for create a document"""


class DocumentUpdateDomain(DocumentAttrs):
    """Domain model definition for update a document"""


class DocumentDomain(DocumentAttrs):
    """
    Domain model definition for a document object

    :note: class will act as a DTO, will be the object to communicate between service and data layer
    """

    class Config:
        from_attributes = True

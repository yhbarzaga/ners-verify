from pydantic.v1 import BaseModel


class ProcessDocumentData(BaseModel):
    """Schema definition used to process a document."""

    file_url: str
    file_name: str
    country: str

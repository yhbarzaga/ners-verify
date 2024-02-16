from pydantic import BaseModel


class DocumentCreateSchema(BaseModel):
    """Schema definition used to create documents from request"""

    file_url: str
    file_name: str
    country: str
    staff_id: str

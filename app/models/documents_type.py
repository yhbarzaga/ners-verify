from sqlalchemy import Column, String, UUID

from app.db.base_class import Base


class DocumentType(Base):
    """Database model definition for documents type."""

    __tablename__ = "documents_type"

    uid: str = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    type: float = Column(String())

    def __repr__(self) -> str:
        return f"<User uid: {self.uid} type: {self.type}>"

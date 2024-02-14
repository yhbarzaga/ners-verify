from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.domain import constants


class Staff(Base):
    """Database model definition for staff."""

    __tablename__ = "staff"

    uid: str = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    internal_id: str = Column(
        String(),
        unique=True,
        nullable=False,
        comment="Stand for the unique identifier of the user inside the ERP",
    )
    documents = relationship("Document")

    def __repr__(self) -> str:
        return f"<User uid: {self.uid} internal_id:{self.internal_id}>"

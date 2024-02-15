import uuid

from sqlalchemy import Column, ForeignKey, DECIMAL, UUID

from app.db.base_class import Base


class Document(Base):
    """Database model definition for documents."""

    __tablename__ = "documents"

    uid: str = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    total: float = Column(DECIMAL(7, 2), default=0, comment="Total to be refunded")
    staff_id: str = Column(UUID(as_uuid=True), ForeignKey("staff.uid"), nullable=False)

    def __repr__(self) -> str:
        return f"<User uid: {self.uid}>"

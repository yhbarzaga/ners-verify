import pendulum
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    """Base class for a data model."""

    __name__: str
    created_at = Column(DateTime, nullable=False, default=pendulum.now("UTC"))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=pendulum.now("UTC"),
        onupdate=pendulum.now("UTC"),
    )

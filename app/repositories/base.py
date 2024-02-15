from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, session: Session):
        """
        Implements data access by encapsulating the set of objects persisted in
        a data store and the operations performed over them.

        :Parameters:
        *session: A SQLAlchemy session instance
        """
        self.session = session

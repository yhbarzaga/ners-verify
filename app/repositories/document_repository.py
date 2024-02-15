from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError

from app.domain.document import (
    DocumentDomain,
    DocumentCreateDomain,
    DocumentUpdateDomain,
)
from app.exceptions import CreationError
from app.models import Document
from app.repositories.base import BaseRepository


class DocumentRepository(
    BaseRepository[Document, DocumentCreateDomain, DocumentUpdateDomain]
):
    """Document repository implementation."""

    def create(self, obj_in: DocumentCreateDomain) -> DocumentDomain:
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = Document(**obj_in_data)
            self.session.add(db_obj)
            self.session.commit()
        except IntegrityError as err:
            self.session.rollback()
            raise CreationError(f"Error trying to create a document, {err}")

        self.session.refresh(db_obj)

        return DocumentDomain.from_orm(db_obj)

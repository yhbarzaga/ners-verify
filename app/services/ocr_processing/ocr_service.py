from typing import Optional

from app.domain import DocumentCreateDomain
from app.repositories import DocumentRepository
from app.services.ocr_processing import OCRProvider, ProcessDocumentData


class OCRService:
    """Composition class to call different OCR providers."""

    def __init__(
        self,
        ocr_provider: Optional[OCRProvider],
        repo: DocumentRepository,
    ):
        """Initialize service."""

        self.repo = repo
        self.ocr_provider = ocr_provider

    def process(self, staff_id: str, document: ProcessDocumentData):
        """Process document through the given provider and save information in a database."""

        new_document = self.ocr_provider.process_document(document)
        self.repo.create(DocumentCreateDomain(staff_id=staff_id, **new_document.dict()))

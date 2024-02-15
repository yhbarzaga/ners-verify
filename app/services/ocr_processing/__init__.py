import abc

from app.services.ocr_processing.ocr_schema import ProcessDocumentData


class OCRProvider(metaclass=abc.ABCMeta):
    """Abstract base class to hold OCR provider methods."""

    @abc.abstractmethod
    def get_document(self, document_id: int):
        """Abstract method to get a document"""
        raise NotImplementedError

    @abc.abstractmethod
    def process_document(self, document: ProcessDocumentData):
        """Abstract method to process a document"""
        raise NotImplementedError

    @abc.abstractmethod
    def update_document(self):
        """Abstract method to update a document"""
        raise NotImplementedError

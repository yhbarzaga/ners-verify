import requests
from requests import HTTPError

from app.services.ocr_processing import OCRProvider, ProcessDocumentData
from app.services.ocr_processing.ocr_entity import (
    OCRProviderId,
    DocumentFromProvider,
    DocumentResponse,
)
from app.services.ocr_processing.ocr_exceptions import OCRDocumentException


class VerifyProvider(OCRProvider):
    """Verify OCR provider implementation."""

    provider_id: int = OCRProviderId.VERIFY.value
    provider_name: str = "Verify"

    def __init__(self, settings):
        """Initialize instance."""

        self.settings = settings
        self.headers = self._set_headers()

    # noinspection PyMethodMayBeStatic
    def _set_headers(self):
        """Set initial headers."""
        return {
            "CLIENT-ID": self.settings.verify_client_id,
            "AUTHORIZATION": f"apikey {self.settings.verify_user_name}:{self.settings.verify_api_key}",
        }

    def get_document(self, document_id: str) -> DocumentFromProvider:
        """Get a document from Verify"""
        response = self._get(path=f"/documents/{document_id}")

        document = DocumentResponse(**response)

        return self._parse_response(document)

    def process_document(self, document: ProcessDocumentData) -> DocumentFromProvider:
        """Process a document trough Verify"""

        response = self._post(path="/documents", json=document.dict())

        document = DocumentResponse(**response)

        return self._parse_response(document)

    def update_document(self):
        """Update a processed document trough Verify"""

    # noinspection PyMethodMayBeStatic
    def _process_request(self, response):
        """Process response and check for errors."""
        data = response.json()

        try:
            response.raise_for_status()
        except HTTPError as err:
            details = f"{data['message']} {data['error']}"
            raise OCRDocumentException(
                detail=details, status_code=response.status_code
            ) from err

        return data

    def _get(self, path: str):
        """Make a get to verify api."""

        url = f"{self.settings.api_base_url}{path}"

        return self._process_request(requests.get(url, headers=self.headers))

    def _post(self, path: str, json: dict = None):
        """Make a post to verify api."""

        url = f"{self.settings.api_base_url}{path}"

        return self._process_request(
            requests.post(url, json=json, headers=self.headers)
        )

    def _parse_response(self, document: DocumentResponse) -> DocumentFromProvider:
        """Parse a document response and return a domain model."""

        return DocumentFromProvider(
            **document.dict(),
            name=self.provider_name,
            provider_id=self.provider_id,
        )

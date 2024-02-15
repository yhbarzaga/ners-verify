from unittest import mock
from unittest.mock import patch

import pytest

from app.services.ocr_processing import ProcessDocumentData
from app.services.ocr_processing.ocr_exceptions import OCRDocumentException
from app.services.ocr_processing.providers import VerifyProvider


class TestVerifyServiceProvider:
    """Test related to Verify OCR provider"""

    def test_get_document_success(self):
        """Test get document from Verify service."""
        response = mock.Mock()
        response.json = lambda: {"id": 999, "total": 99}

        service = VerifyProvider(
            settings=mock.Mock(
                api_base_url="https://verify.api.com",
                client_id="my_client_id",
                client_secret="my_client_secret",
                api_key="my_api_key",
                user_name="my_user_name",
            )
        )

        document_id = "my_document_id"
        with mock.patch(
            "app.services.ocr_processing.providers.verify.verify_provider.requests.get",
            return_value=response,
        ) as m_get:
            service.get_document(document_id)

            m_get.assert_called_with(
                f"https://verify.api.com/documents/{document_id}",
                headers={
                    "CLIENT-ID": "my_client_id",
                    "AUTHORIZATION": "apikey my_user_name:my_api_key",
                },
            )

    @patch(
        "app.services.ocr_processing.providers.verify.verify_provider.VerifyProvider._process_request"
    )
    @patch("app.services.ocr_processing.providers.verify.verify_provider.requests.get")
    def test_get_document_reach_rate_limit(self, mock_request, mock_process):
        """Test that try to get a document when the rate limit is being reached will response with error."""

        response = mock.Mock()
        response.raise_for_status.side_effect = Exception()

        mock_request.return_value = response
        mock_process.side_effect = OCRDocumentException(
            429, "You have been rate limited"
        )

        service = VerifyProvider(
            settings=mock.Mock(
                api_base_url="https://verify.api.com",
                client_id="my_client_id",
                client_secret="my_client_secret",
                api_key="my_api_key",
                user_name="my_user_name",
            )
        )

        document_id = "my_document_id"
        with pytest.raises(OCRDocumentException) as exc:
            service.get_document(document_id)

        assert exc.value.detail == "You have been rate limited"
        mock_request.assert_called_with(
            f"https://verify.api.com/documents/{document_id}",
            headers={
                "CLIENT-ID": "my_client_id",
                "AUTHORIZATION": "apikey my_user_name:my_api_key",
            },
        )

    def test_process_document_success(self):
        """Test success document processing from Verify service."""
        mock_response = {"id": 999, "total": 99}
        response = mock.Mock()
        response.json = lambda: mock_response

        service = VerifyProvider(
            settings=mock.Mock(
                api_base_url="https://verify.api.com",
                client_id="my_client_id",
                client_secret="my_client_secret",
                api_key="my_api_key",
                user_name="my_user_name",
            )
        )

        document = ProcessDocumentData(
            file_url="https://myawesome.url",
            file_name="myAwesomeFileName",
            country="US",
        )

        with mock.patch(
            "app.services.ocr_processing.providers.verify.verify_provider.requests.post",
            return_value=response,
        ) as m_get:
            result = service.process_document(document)

            m_get.assert_called_with(
                "https://verify.api.com/documents",
                headers={
                    "CLIENT-ID": "my_client_id",
                    "AUTHORIZATION": "apikey my_user_name:my_api_key",
                },
                json={
                    "file_url": document.file_url,
                    "file_name": document.file_name,
                    "country": document.country,
                },
            )

            assert result.id == mock_response["id"]
            assert result.total == mock_response["total"]
            assert result.name == "Verify"
            assert result.provider_id == 1

    @patch(
        "app.services.ocr_processing.providers.verify.verify_provider.VerifyProvider._process_request"
    )
    @patch("app.services.ocr_processing.providers.verify.verify_provider.requests.post")
    def test_process_document_bad_request(self, mock_request, mock_process):
        """Test that process document fail."""

        response = mock.Mock()
        response.raise_for_status.side_effect = Exception()

        mock_request.return_value = response
        mock_process.side_effect = OCRDocumentException(
            400, "Couldn't download file from provided url."
        )

        service = VerifyProvider(
            settings=mock.Mock(
                api_base_url="https://verify.api.com",
                client_id="my_client_id",
                client_secret="my_client_secret",
                api_key="my_api_key",
                user_name="my_user_name",
            )
        )

        document = ProcessDocumentData(
            file_url="https://myawesome.url",
            file_name="myAwesomeFileName",
            country="US",
        )
        with pytest.raises(OCRDocumentException) as exc:
            service.process_document(document)

        assert exc.value.detail == "Couldn't download file from provided url."
        mock_request.assert_called_with(
            "https://verify.api.com/documents",
            headers={
                "CLIENT-ID": "my_client_id",
                "AUTHORIZATION": "apikey my_user_name:my_api_key",
            },
            json={
                "file_url": document.file_url,
                "file_name": document.file_name,
                "country": document.country,
            },
        )

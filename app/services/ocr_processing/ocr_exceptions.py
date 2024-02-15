class OCRDocumentException(Exception):
    """General exception for OCR providers response."""

    def __init__(self, status_code: int, detail: str = None):
        """Initialize exception wrapper data."""

        super().__init__()

        self.status_code = status_code
        self.detail = detail

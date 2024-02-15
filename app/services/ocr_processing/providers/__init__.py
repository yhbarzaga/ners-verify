from app.services.ocr_processing.providers.verify import VerifyProvider, VerifySettings


provider_map = {1: VerifyProvider}
provider_settings_map = {1: VerifySettings}


def get_ocr_provider(provider_id: int = 1):
    """
    Return OCR provider.
    :note: in future this function should be modified to support new providers
    """
    provider_cls = provider_map[provider_id]
    return provider_cls(settings=_get_ocr_provider_settings(provider_id))


def _get_ocr_provider_settings(provider_id: int):
    """Return OCR provider settings."""

    setting_cls = provider_settings_map[provider_id]
    return setting_cls()

from app.services.ocr_processing.providers.verify import VerifyProvider, VerifySettings


provider_map = {1: VerifyProvider}
provider_settings_map = {1: VerifySettings}
provider_id = 1  # this fixed provider need to be defined in a more dynamic way


def get_ocr_provider():
    """
    Return OCR provider.
    :note: in future this function should be modified to support new providers
    """
    provider_cls = provider_map[provider_id]
    return provider_cls(settings=_get_ocr_provider_settings(provider_id))


def _get_ocr_provider_settings(key: int):
    """Return OCR provider settings."""

    setting_cls = provider_settings_map[key]
    return setting_cls()

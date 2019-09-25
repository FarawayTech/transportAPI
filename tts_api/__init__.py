from .api import BaseTTSApi
from .google_tts_api import GoogleTTSApi


def get_api() -> BaseTTSApi:
    return GoogleTTSApi()

from .api import BaseUVIApi
from .bitweather_api import BitWeatherApi


def get_api() -> BaseUVIApi:
    return BitWeatherApi()

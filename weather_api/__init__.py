from .api import BaseWeatherApi
from .open_weather_api import OpenWeatherApi


def get_api() -> BaseWeatherApi:
    return OpenWeatherApi()

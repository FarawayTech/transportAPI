from abc import ABC, abstractmethod

from stations import GeoPoint


class BaseWeatherApi(ABC):
    @abstractmethod
    def get_forecast(self, location: GeoPoint):
        pass

    @abstractmethod
    def get_uv_index(self, location: GeoPoint):
        pass
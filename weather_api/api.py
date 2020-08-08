from abc import ABC, abstractmethod

from stations import GeoPoint


class BaseWeatherApi(ABC):
    @abstractmethod
    def get_forecast(self, location: GeoPoint):
        pass

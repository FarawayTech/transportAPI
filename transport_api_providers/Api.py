from abc import ABC, abstractmethod

from stations import Station


class Api(ABC):
    @abstractmethod
    def get_departures(self, station: Station, time):
        pass

    @abstractmethod
    def get_connections(self, origin: str, destination: str, time, limit: int):
        pass

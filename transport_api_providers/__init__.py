from .sbb.SBBApi import SBBApi
from .Api import Api


def get_api(station_id: str) -> Api:
    return SBBApi()

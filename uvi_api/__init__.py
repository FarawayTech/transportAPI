from .api import BaseUVIApi
from .openuv_api import OpenUVApi


def get_api() -> BaseUVIApi:
    return OpenUVApi()

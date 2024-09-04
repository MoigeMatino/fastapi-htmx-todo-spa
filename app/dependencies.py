import os
from functools import lru_cache

from .config import Settings, TestSettings

# from sqlmodel import Session
# from .db import engine


# ! TUsed as a dependency injection in requests
# ? Why?
# * to provide a different settings object during testing by creating a
# * dependency override for get_settings
# * require it from path operation functions as a dependency and use it
# * anywhere we need it.
# ? Why lru_cache
# * Reading a file from disk is normally a costly (slow) operation so its
# * better to do it once then
# * reuse the same settings object, instead of reading it for each request.
@lru_cache
def get_settings():
    return Settings()


def get_test_settings():
    print(f"Current working directory: {os.getcwd()}")
    return TestSettings()

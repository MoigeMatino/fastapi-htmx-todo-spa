from functools import lru_cache  # noqa: F401

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    db_host: str
    db_port: str

    model_config = SettingsConfigDict(env_file=".env")


# ! To be used as a dependency injection in requests
# ? Why?
# * to provide a different settings object during testing by creating a
# * dependency override for get_settings
# * require it from path operation functions as a dependency and use it
# * anywhere we need it.
# ? Why lru_cache
# * Reading a file from disk is normally a costly (slow) operation so its
# * better to do it once then
# * reuse the same settings object, instead of reading it for each request.
# @lru_cache
# def get_settings():
#     return Settings()

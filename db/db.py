from sqlmodel import SQLModel, create_engine

from config import Settings

from .. import models  # noqa: F401

settings = Settings()

DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_engine(DATABASE_URL, echo=True)

SQLModel.metadata.create_all(engine)

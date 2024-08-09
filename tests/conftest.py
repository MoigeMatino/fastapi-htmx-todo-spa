import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app import app
from app.db import get_session
from app.dependencies import get_test_settings
from app.models.todo import Todo, TodoCreate  # noqa: F401
from app.utils.todo import db_create_todo


@pytest.fixture(scope="session")
def test_settings():
    return get_test_settings()


@pytest.fixture(scope="session")
def engine(test_settings):
    engine = create_engine(
        f"postgresql://{test_settings.postgres_user}:{test_settings.postgres_password}@{test_settings.db_host}/{test_settings.postgres_db}",  # noqa: E501
        echo=True,
    )
    return engine


@pytest.fixture(scope="session")
def create_test_database(engine):
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


# fixture to create a new session for each test
@pytest.fixture(scope="function")
def session(engine, create_test_database):
    with Session(engine) as session:
        yield session


# fixture provides a TestClient through which API calls can use the test database session.
@pytest.fixture(scope="function")
def client(session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}


# fixture that directly provides a test database session to tests
@pytest.fixture(name="override_session")
def override_session_fixture(session: Session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    yield session
    app.dependency_overrides = {}


@pytest.fixture(name="create_todo")
def create_todo_fixture(override_session) -> Todo:
    todo_data = TodoCreate(title="Test Todo Item")
    todo = db_create_todo(override_session, todo_data)
    return todo

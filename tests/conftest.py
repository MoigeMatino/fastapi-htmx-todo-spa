from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app import app
from app.db import get_session
from app.dependencies import get_test_settings
from app.models.todo import Todo, TodoCreate  # noqa: F401
from app.models.user import UserCreate
from app.utils.todo import db_create_todo
from app.utils.user import create_user_in_db


@pytest.fixture(scope="session")
def test_settings():
    return get_test_settings()


@pytest.fixture(scope="session")
def test_engine(test_settings):
    test_database_url = (
        f"postgresql://{test_settings.postgres_user}:{test_settings.postgres_password}"
        f"@{test_settings.db_host}/{test_settings.postgres_db}"
    )
    engine = create_engine(test_database_url, echo=True)
    return engine


# Fixture to create a new session for each test with cleanup
@pytest.fixture(scope="function")
def session(test_engine):
    # Clean up the database before each test
    SQLModel.metadata.drop_all(bind=test_engine)
    SQLModel.metadata.create_all(bind=test_engine)

    with Session(test_engine) as session:
        yield session

    # Optionally clean up after the test
    SQLModel.metadata.drop_all(bind=test_engine)


# Fixture that directly provides a test database session to tests
@pytest.fixture(name="override_session")
def override_session_fixture(session: Session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    yield session
    app.dependency_overrides = {}


# Fixture provides a TestClient through which API calls can use the test database session
@pytest.fixture(scope="function")
def client(override_session):
    def override_get_session():
        return override_session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}


# Fixture for creating a test todo
@pytest.fixture(name="test_todo", scope="function")
def create_todo_fixture(override_session) -> Todo:
    todo_data = TodoCreate(title="Test Todo Item")
    todo = db_create_todo(override_session, todo_data)
    return todo


# Fixture for creating a test user
@pytest.fixture(name="test_user", scope="function")
def test_user_fixture(override_session):
    unique_username = f"test_user_{uuid4()}"
    user_data = UserCreate(username=unique_username, password="password123")
    user = create_user_in_db(user_data.username, user_data.password, override_session)
    return user


# Fixture for creating a user and a todo associated with that user
@pytest.fixture(name="user_and_todo", scope="function")
def user_and_todo_fixture(test_user, override_session):
    todo_data = TodoCreate(title="Test Todo Item")
    todo = db_create_todo(override_session, todo_data, test_user.id)
    return test_user, todo

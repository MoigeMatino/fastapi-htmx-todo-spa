from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

# from app import create_app
from app import app
from app.db import get_session
from app.models.todo import Todo, TodoCreate  # noqa: F401
from app.models.user import UserCreate
from app.utils.jwt import create_access_token
from app.utils.todo import db_create_todo
from app.utils.user import create_user_in_db

# @pytest.fixture(scope="session")
# def test_settings():
#     settings = TestSettings()
#     print(f"Test settings: {settings.model_dump()}")
#     return settings


@pytest.fixture(scope="session")
def test_engine():
    test_database_url = (
        "postgresql://test_user:test_password@test_db/fastapi_todo_test_db"
    )

    engine = create_engine(test_database_url, echo=True)
    return engine


@pytest.fixture(scope="function")
def session(test_engine):
    # Clean up the database before each test
    SQLModel.metadata.drop_all(bind=test_engine)
    SQLModel.metadata.create_all(bind=test_engine)

    with Session(test_engine) as session:
        yield session

    SQLModel.metadata.drop_all(bind=test_engine)


# Fixture that directly provides a test database session to tests
@pytest.fixture(name="override_session")
def override_session_fixture(session: Session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    yield session
    app.dependency_overrides.pop(get_session, None)


# Fixture provides a TestClient through which API calls can use the test database session
@pytest.fixture(scope="function")
def client(override_session):
    def override_get_session():
        return override_session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.pop(get_session, None)


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


@pytest.fixture
def logged_in_user(override_session):
    # Create a test user
    user_data = UserCreate(username="test_user", password="password123")
    user = create_user_in_db(user_data.username, user_data.password, override_session)

    # Generate a token or session data directly
    token = create_access_token({"sub": user.username})

    return {"cookie": token, "user_id": user.id, "username": user.username}

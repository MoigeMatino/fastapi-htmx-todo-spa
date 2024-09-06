from app.models.user import UserCreate
from app.utils.user import create_user_in_db  # noqa: F401


def test_signup(client):
    response = client.post(
        "/auth/signup", data={"username": "newuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["success"]


def test_signup_existing_user(client):
    # initial signup request made by newuser
    response = client.post(
        "/auth/signup", data={"username": "newuser", "password": "password123"}
    )

    # Second signup request made by existing user
    response = client.post(
        "/auth/signup", data={"username": "newuser", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already taken"}


def test_signup_missing_username(client):
    response = client.post("/auth/signup", data={"password": "password123"})

    assert response.status_code == 422
    assert "detail" in response.json()
    assert "Field required" in response.json()["detail"][0]["msg"]


def test_signup_missing_password(client):
    response = client.post("/auth/signup", data={"username": "newuser"})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert "Field required" in response.json()["detail"][0]["msg"]


def test_signup_empty_data(client):
    response = client.post("/auth/signup", data={})

    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"][0]["loc"] == ["body", "username"]
    assert response.json()["detail"][1]["loc"] == ["body", "password"]


def test_login(client, override_session):
    user_data = UserCreate(username="test_user", password="password123")
    create_user_in_db(user_data.username, user_data.password, override_session)

    # Test with valid credentials
    response = client.post(
        "/auth/login",
        data={"username": "test_user", "password": "password123"},
        allow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/?username=test_user"
    assert "Authorization" in response.cookies


def test_login_invalid_credentials(client, override_session):
    user_data = UserCreate(username="test_user", password="password123")
    create_user_in_db(user_data.username, user_data.password, override_session)
    # Test with invalid credentials
    response = client.post(
        "auth/login", data={"username": "nonexistent", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Authorization" not in response.cookies
    assert response.json() == {"detail": "Incorrect username or password"}


def test_logout(client):
    response = client.get(
        "/auth/logout",
        allow_redirects=False,
    )
    assert response.status_code == 302
    assert "Authorization" not in response.cookies


def test_get_me_authenticated(client, logged_in_user):
    cookies = {"Authorization": logged_in_user["cookie"]}
    response = client.get("/auth/me", cookies=cookies)
    assert response.status_code == 200
    assert "username" in response.json()


def test_check_auth_valid_logged_in_user(client, logged_in_user):
    cookies = {"Authorization": logged_in_user["cookie"]}

    response = client.get("/auth/check-auth", cookies=cookies)
    assert response.status_code == 200
    assert response.json()["status"] == "valid"


def test_check_auth_valid_non_logged_in_user(client):
    response = client.get("/auth/check-auth")
    assert response.status_code == 200
    assert response.json()["status"] == "unauthorised"

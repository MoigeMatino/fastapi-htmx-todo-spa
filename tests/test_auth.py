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


# def test_login(client, override_session):
#     create_user_in_db("test_user","password123", override_session)
#     # Test with valid credentials
#     response = client.post(
#         "/auth/login", data={"username": "test_user", "password": "password123"}
#     )
#     import pdb; pdb.set_trace()
#     assert response.status_code == 200


#     # Test with invalid password
#     response = client.post(
#         "/auth/login", data={"username": "test_user", "password": "password124"}
#     )
#     import pdb; pdb.set_trace()

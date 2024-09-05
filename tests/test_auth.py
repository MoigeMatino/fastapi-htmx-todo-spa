from app.utils.user import create_user_in_db  # noqa: F401


def test_signup(client):
    response = client.post(
        "/auth/signup", data={"username": "newuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["success"]


def test_signup_existing_user(client):
    response = client.post(
        "/auth/signup", data={"username": "newuser", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already taken"}

    # Test with missing username
    response = client.post("/auth/signup", data={"password": "password123"})

    assert response.status_code == 422
    assert "detail" in response.json()
    assert "Field required" in response.json()["detail"][0]["msg"]

    # Test with missing password
    response = client.post("/auth/signup", data={"username": "newuser"})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert "Field required" in response.json()["detail"][0]["msg"]

    # Test with empty data
    response = client.post("/auth/signup", data={})

    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"][0]["loc"] == ["body", "username"]
    assert response.json()["detail"][1]["loc"] == ["body", "password"]


# def test_login_(client, override_session):
#     create_user_in_db("test_user","password123", override_session)
#     # Test with valid credentials
#     response = client.post(
#         "/auth/login", data={"username": "test_user", "password": "password123"}
#     )
#     import pdb; pdb.set_trace()
#     assert response.status_code == 303
#     assert response.headers["Location"] == "http://localhost/?username=test_user"
#     assert "Authorization" in response.cookies

#     # Test with invalid password
#     response = client.post(
#         "/auth/login", data={"username": "test_user", "password": "password124"}
#     )
#     import pdb; pdb.set_trace()

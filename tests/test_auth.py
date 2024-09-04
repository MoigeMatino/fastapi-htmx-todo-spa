def test_signup(client):
    response = client.post(
        "/auth/signup", data={"username": "newuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["success"]

    # test signup for an existing user
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

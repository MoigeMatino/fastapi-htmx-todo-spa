from app.models.todo import TodoCreate
from app.utils.todo import db_create_todo


def test_list_todos(client, override_session, logged_in_user):
    todo_1_data = TodoCreate(title="Test Todo 1")
    todo_2_data = TodoCreate(title="Test Todo 2")

    db_create_todo(override_session, todo_1_data, logged_in_user["user_id"])
    db_create_todo(override_session, todo_2_data, logged_in_user["user_id"])

    cookies = {"Authorization": logged_in_user["cookie"]}
    response = client.get("/todos", cookies=cookies)
    assert response.status_code == 200
    assert "Test Todo 1" in response.text
    assert "Test Todo 2" in response.text

    hx_response = client.get("/todos", headers={"HX-Request": "true"}, cookies=cookies)
    assert hx_response.status_code == 200
    assert "Test Todo 1" in hx_response.text
    assert "Test Todo 2" in hx_response.text


def test_create_todo(client, logged_in_user):
    cookies = {"Authorization": logged_in_user["cookie"]}

    response = client.post("/todos", data={"todo": "New Todo"}, cookies=cookies)
    assert response.status_code == 200
    assert "New Todo" in response.text


def test_update_todo(client, override_session, logged_in_user):
    todo_data = TodoCreate(title="Old Title")
    todo = db_create_todo(override_session, todo_data, logged_in_user["user_id"])

    cookies = {"Authorization": logged_in_user["cookie"]}
    response = client.put(
        f"/todos/{todo.id}", data={"title": "New Title"}, cookies=cookies
    )

    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo[0]["title"] == "New Title"
    assert updated_todo[0]["user_id"] == logged_in_user["user_id"]


def test_toggle_todo(client, override_session, logged_in_user):
    todo_data = TodoCreate(title="Toggle Todo")
    todo = db_create_todo(override_session, todo_data, logged_in_user["user_id"])

    cookies = {"Authorization": logged_in_user["cookie"]}
    response = client.post(f"/todos/{todo.id}/toggle", cookies=cookies)
    assert response.status_code == 200
    toggled_todo = response.json()
    assert toggled_todo[0]["done"] is True
    assert toggled_todo[0]["title"] == "Toggle Todo"
    assert toggled_todo[0]["user_id"] == logged_in_user["user_id"]

    # Toggle back
    response = client.post(f"/todos/{todo.id}/toggle", cookies=cookies)
    assert response.status_code == 200
    toggled_todo = response.json()
    assert toggled_todo[0]["done"] is False
    assert toggled_todo[0]["title"] == "Toggle Todo"


def test_delete_todo(client, override_session, logged_in_user):
    todo_data = TodoCreate(title="Delete Todo")
    todo = db_create_todo(override_session, todo_data, logged_in_user["user_id"])

    cookies = {"Authorization": logged_in_user["cookie"]}

    response = client.delete(f"/todos/{todo.id}/delete", cookies=cookies)
    assert response.status_code == 200

    # Verify that the todo was deleted
    response = client.get("/todos", cookies=cookies)
    assert response.status_code == 200
    assert "Delete Todo" not in response.text


def test_db_connection(override_session):
    print(f"Connected to database: {override_session.bind.url}")
    assert "test_db" in str(override_session.bind.url)

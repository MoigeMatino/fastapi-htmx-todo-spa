from app.models import TodoCreate
from app.utils import db_create_todo


def test_list_todos(client, override_session):
    todo_1_data = TodoCreate(title="Test Todo 1")
    todo_2_data = TodoCreate(title="Test Todo 2")

    db_create_todo(override_session, todo_1_data)
    db_create_todo(override_session, todo_2_data)

    response = client.get("/todos")
    assert response.status_code == 200
    assert "Test Todo 1" in response.text
    assert "Test Todo 2" in response.text

    hx_response = client.get("/todos", headers={"HX-Request": "true"})
    assert hx_response.status_code == 200
    assert "Test Todo 1" in hx_response.text
    assert "Test Todo 2" in hx_response.text

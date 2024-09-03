from sqlmodel import select

from app.models.todo import Todo, TodoCreate
from app.utils.todo import (
    db_create_todo,
    db_delete_todo,
    db_toggle_todo,
    db_update_todo,
)


def test_db_create_todo(override_session, test_user):
    todo_data = TodoCreate(title="Test Todo Item")
    todo = db_create_todo(override_session, todo_data, test_user.id)

    assert todo is not None
    assert todo.title == "Test Todo Item"
    assert todo.user_id is not None
    assert todo.user_id == test_user.id


def test_db_update_todo(override_session, user_and_todo):
    test_user, test_todo = user_and_todo

    updated_todo_title = "Updated Test Todo Item"
    updated_todo = db_update_todo(override_session, test_todo.id, updated_todo_title)

    assert updated_todo is not None
    assert updated_todo.id == test_todo.id
    assert updated_todo.user_id == test_user.id
    assert updated_todo.title == "Updated Test Todo Item"


def test_db_toggle_todo(override_session, user_and_todo):
    test_user, test_todo = user_and_todo

    toggled_todo = db_toggle_todo(override_session, test_todo.id)

    assert toggled_todo is not None
    assert toggled_todo.id == test_todo.id
    assert toggled_todo.user_id == test_user.id
    assert toggled_todo.done


def test_db_delete_todo(override_session, user_and_todo):
    _, test_todo = user_and_todo

    db_delete_todo(override_session, test_todo.id)
    deleted_todo = override_session.exec(
        select(Todo).where(Todo.id == test_todo.id)
    ).first()
    assert deleted_todo is None

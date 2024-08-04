from sqlmodel import select

from app.models import Todo, TodoCreate
from app.utils import db_create_todo, db_delete_todo, db_toggle_todo, db_update_todo


def test_db_create_todo(override_session):
    todo_data = TodoCreate(title="Test Todo Item")
    todo = db_create_todo(override_session, todo_data)

    assert todo is not None
    assert todo.title == "Test Todo Item"


def test_db_update_todo(override_session):
    todo_data = TodoCreate(title="Test Todo Item")
    todo = db_create_todo(override_session, todo_data)

    updated_todo_title = "Updated Test Todo Item"
    updated_todo = db_update_todo(override_session, todo.id, updated_todo_title)

    assert updated_todo is not None
    assert updated_todo.id == todo.id
    assert updated_todo.title == "Updated Test Todo Item"


def test_db_toggle_todo(override_session):
    todo_data = TodoCreate(title="Test Todo Item", done=True)
    todo = db_create_todo(override_session, todo_data)

    toggled_todo = db_toggle_todo(override_session, todo.id)

    assert toggled_todo is not None
    assert toggled_todo.id == todo.id
    assert not toggled_todo.done


def test_db_delete_todo(override_session):
    todo_data = TodoCreate(title="Test Todo Item")
    todo = db_create_todo(override_session, todo_data)

    db_delete_todo(override_session, todo.id)
    deleted_todo = override_session.exec(select(Todo).where(Todo.id == todo.id)).first()
    assert deleted_todo is None

import os

import aiofiles

from app.utils.todo import get_todo_by_id

UPLOAD_DIR = "uploads"


async def upload_file(file_content: bytes, filename: str, todo_id: str):
    from app.db import SessionLocal

    session = None
    try:
        session = SessionLocal()

        # Ensure the upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Create the file path
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save the file with the content provided
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(file_content)

        # Update the todo with the uploaded file path
        todo = get_todo_by_id(session, todo_id)
        todo.file_name = filename
        todo.file_path = file_path

        session.add(todo)
        session.commit()

    except Exception as e:
        print(f"Error: {e}")
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()

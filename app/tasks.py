import os

from fastapi import UploadFile

from app.utils.todo import get_todo_by_id

UPLOAD_DIR = "uploads"


async def upload_file(file: UploadFile, todo_id: str):
    from app.db import SessionLocal

    with SessionLocal() as session:
        # Ensure the upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Generate a unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{todo_id}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save the file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Update the todo with the uploaded file path
        todo = get_todo_by_id(session, todo_id)
        todo.file_name = unique_filename
        # TODO: replace file_url with file_path
        todo.file_url = file_path
        session.add(todo)
        session.commit()

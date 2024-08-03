from contextlib import asynccontextmanager
from typing import Annotated, Union

from fastapi import Depends, FastAPI, Form, Header, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.database.db import get_session, init_db
from app.models import TodoCreate
from app.utils import (
    db_create_todo,
    db_delete_todo,
    db_get_todos,
    db_toggle_todo,
    db_update_todo,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/todos", response_class=HTMLResponse)
async def list_todos(
    request: Request,
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
):
    todos = db_get_todos(session)
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@app.post("/todos", response_class=HTMLResponse)
async def create_todo(
    request: Request,
    todo: Annotated[str, Form()],  # form parsing
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
):
    # Parse form data into `TodoCreate` data model for validation
    todo_data = TodoCreate(title=todo)

    try:
        # Create an instance of `Todo` from the validated `TodoCreate` data
        db_create_todo(session, todo_data)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    # Fetch the updated list of todos
    todos = db_get_todos(session)

    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@app.put("/todos/{todo_id}", response_class=HTMLResponse)
async def update_todo(
    request: Request,
    todo_id: str,
    title: Annotated[str, Form()],
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
):
    try:
        db_update_todo(session, todo_id, title)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    # Fetch the updated list of todos
    todos = db_get_todos(session)
    # Render the updated list of todos
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@app.post("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(
    request: Request,
    todo_id: str,
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
):
    try:
        db_toggle_todo(session, todo_id)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    # Fetch the updated list of todos
    todos = db_get_todos(session)

    # Render the updated list of todos
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@app.delete("/todos/{todo_id}/delete", response_class=HTMLResponse)
async def delete_todo(
    request: Request,
    todo_id: str,
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
):
    try:
        db_delete_todo(session, todo_id)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    todos = db_get_todos(session)
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))

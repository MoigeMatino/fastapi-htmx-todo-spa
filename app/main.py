from contextlib import asynccontextmanager
from typing import Annotated, Union

from fastapi import Depends, FastAPI, Form, Header, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.database.db import get_session, init_db
from app.models import Todo, TodoCreate
from app.utils import add_todo, get_todos


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
    todos = get_todos(session)
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
        add_todo(session, todo_data)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    # Fetch the updated list of todos
    todos = get_todos(session)

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
    # Query the todo item by ID
    todo = session.exec(select(Todo).where(Todo.id == todo_id)).first()
    if not todo:
        return JSONResponse(content={"error": "Todo not found"}, status_code=404)

    # Update the title
    todo.title = title

    # Commit changes
    session.add(todo)
    session.commit()
    session.refresh(todo)

    # Fetch the updated list of todos
    todos = session.exec(select(Todo)).all()
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
    # Query the todo item by ID
    todo = session.exec(select(Todo).where(Todo.id == todo_id)).first()
    if not todo:
        return JSONResponse(content={"error": "Todo not found"}, status_code=404)

    # Toggle the done status
    todo.done = not todo.done

    # Commit changes
    session.add(todo)
    session.commit()
    session.refresh(todo)

    # Fetch the updated list of todos
    todos = session.exec(select(Todo)).all()

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
    statement = select(Todo).where(Todo.id == todo_id)
    results = session.exec(statement)
    todo = results.one()
    session.delete(todo)
    session.commit()

    todos = session.exec(select(Todo)).all()

    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))

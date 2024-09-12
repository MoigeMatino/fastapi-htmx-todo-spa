from typing import Annotated, Union

from fastapi import APIRouter, Depends, Form, Header, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.db import get_session
from app.models.todo import TodoCreate
from app.models.user import User
from app.routes.user import check_auth
from app.utils.jwt import verify_token
from app.utils.todo import (
    db_create_todo,
    db_delete_todo,
    db_get_user_todos,
    db_toggle_todo,
    db_update_todo,
)
from app.utils.user import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # username = request.query_params.get("username", "")
    auth_status = await check_auth(request)
    auth_status_value = auth_status.get("status")
    is_authenticated = False
    username = None

    if auth_status_value == "valid":
        token = request.cookies.get("Authorization", "").replace("Bearer ", "")
        payload = verify_token(token)
        is_authenticated = True
        username = payload["data"].get("sub")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "is_authenticated": is_authenticated,
            "username": username,
        },
    )


@router.get("/todos", response_class=HTMLResponse)
async def list_todos(
    request: Request,
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    todos = db_get_user_todos(session, current_user.id)
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@router.post("/todos", response_class=HTMLResponse)
async def create_todo(
    request: Request,
    todo: Annotated[str, Form()],  # form parsing
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Parse form data into `TodoCreate` data model for validation
    todo_data = TodoCreate(title=todo)

    try:
        db_create_todo(session, todo_data, current_user.id)

    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    todos = db_get_user_todos(session, current_user.id)

    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@router.put("/todos/{todo_id}", response_class=HTMLResponse)
async def update_todo(
    request: Request,
    todo_id: str,
    title: Annotated[str, Form()],
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        db_update_todo(session, todo_id, title)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    # Fetch the updated list of todos
    todos = db_get_user_todos(session, current_user.id)
    # Render the updated list of todos
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@router.post("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(
    request: Request,
    todo_id: str,
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        db_toggle_todo(session, todo_id)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    # Fetch the updated list of todos
    todos = db_get_user_todos(session, current_user.id)

    # Render the updated list of todos
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@router.delete("/todos/{todo_id}/delete", response_class=HTMLResponse)
async def delete_todo(
    request: Request,
    todo_id: str,
    hx_request: Annotated[Union[str, None], Header()] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        db_delete_todo(session, todo_id)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    todos = db_get_user_todos(session, current_user.id)
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@router.get("/test-user")
def test_user(current_user: User = Depends(get_current_user)):
    return current_user

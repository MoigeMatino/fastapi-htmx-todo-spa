from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.db import get_session
from app.models.user import UserResponse
from app.utils.jwt import create_access_token
from app.utils.user import authenticate_user, create_user_in_db, get_user_by_username

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/signup", response_model=UserResponse)
def signup(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    # check if user exists
    existing_user = get_user_by_username(username, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # if user doesn't exist, create user in the database
    new_user = create_user_in_db(username, password, session)
    return UserResponse(id=new_user.id, username=new_user.username)


@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> RedirectResponse:
    # authenticate user
    authenticated_user = authenticate_user(
        form_data.username, form_data.password, session
    )
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": authenticated_user.username})
    # Create a redirect response
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    # Set the authorization cookie
    response.set_cookie(
        key="Authorization", value=f"Bearer {access_token}", httponly=True
    )

    return response


@router.get("/signup-login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

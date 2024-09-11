from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.db import get_session
from app.models.user import User
from app.utils.jwt import create_access_token, verify_token
from app.utils.user import (
    authenticate_user,
    create_user_in_db,
    get_current_user,
    get_user_by_username,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/signup")
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
    create_user_in_db(username, password, session)
    return {"success": True, "message": "Signup successful! Please log in."}


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
    response = RedirectResponse(
        # url=f"/?username={authenticated_user.username}",
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    # Set the authorization cookie
    response.set_cookie(
        key="Authorization", value=f"Bearer {access_token}", httponly=True
    )

    return response


@router.get("/signup-login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="signup-login", status_code=302)
    response.delete_cookie("Authorization")
    return response


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return current_user


@router.get("/check-auth")
async def check_auth(request: Request):
    token = request.cookies.get("Authorization")

    if not token:
        return {"status": "unauthorised"}

    # Remove the "Bearer " prefix if it exists
    token = token.replace("Bearer ", "")

    token_status = verify_token(token)

    if not token_status:
        return {"status": "unauthorised"}

    if token_status["status"] == "expired":
        return {
            "status": "expired",
            "message": "Your session has expired. Please log in again.",
        }

    return {"status": "valid", "message": "Token is valid"}

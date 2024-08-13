from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db import get_session
from app.models.user import UserCreate, UserResponse
from app.utils.jwt import create_access_token
from app.utils.user import authenticate_user, create_user_in_db, get_user_by_username

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    # check if user exists
    existing_user = get_user_by_username(user.username, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # if user doesn't exist, create user in the database
    new_user = create_user_in_db(user.username, user.password, session)
    return UserResponse(id=new_user.id, username=new_user.username)


@router.post("/login")
def login(user: UserCreate, session: Session = Depends(get_session)):
    # authenticate user
    authenticated_user = authenticate_user(user.username, user.password, session)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": authenticated_user.id})
    return {"access_token": access_token}

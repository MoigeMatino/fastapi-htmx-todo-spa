from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models.user import User, UserCreate, UserResponse
from app.utils.jwt import create_access_token
from app.utils.user import get_user_by_username, hash_password, verify_password

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    # check if user exists
    existing_user = get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # if user doesn't exist, create user in the database
    # TODO: create util to create user in db
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return UserResponse(id=new_user.id, username=new_user.username)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}",
        )


@router.post("/login")
def login(user: UserCreate, session: Session = Depends(get_session)):
    # TODO: add auhtneticate user utility function
    # check if user exists and verify password
    statement = select(User).where(User.username == user.username)
    existing_user = session.exec(statement).first()
    if not existing_user or not verify_password(
        existing_user.hashed_password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": existing_user.id})
    return {"access_token": access_token}

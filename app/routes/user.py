from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models.user import User, UserCreate, UserResponse
from app.utils.user import hash_password

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    # check if user exists
    # TODO: create util to get user by username
    statement = select(User).where(User.username == user.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    # is user doesn't exist, create user in the database
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

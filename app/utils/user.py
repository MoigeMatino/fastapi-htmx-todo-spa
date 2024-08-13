import bcrypt
from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.user import User


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
    hashed_password_string = hashed_password.decode()
    return hashed_password_string


def verify_password(stored_hash_password: str, password: str) -> bool:
    stored_hash = stored_hash_password.encode()

    return bcrypt.checkpw(password.encode(), stored_hash)


def get_user_by_username(username: str, session: Session):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user


def create_user_in_db(username: str, password: str, session: Session):
    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password)
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}",
        )


def authenticate_user(username: str, password: str, session: Session):
    # retrieve user from db
    user = get_user_by_username(username, session)
    if user is None:
        return None

    # verify user password
    if not verify_password(user.hashed_password, password):
        return None

    return user

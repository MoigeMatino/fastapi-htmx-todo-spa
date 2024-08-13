import bcrypt
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

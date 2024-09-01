import bcrypt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session, select

from app.db import get_session
from app.models.token import TokenData
from app.models.user import User
from app.utils.jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    """
    Hashes the provided password using bcrypt with a cost factor of 12.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
    hashed_password_string = hashed_password.decode()
    return hashed_password_string


def verify_password(stored_hash_password: str, password: str) -> bool:
    """
    Verifies the provided password against the stored password hash.

    Args:
        stored_hash_password (str): The stored password hash.
        password (str): The password to be verified.

    Returns:
        bool: True if the provided password matches the stored hash, False otherwise.
    """
    stored_hash = stored_hash_password.encode()

    return bcrypt.checkpw(password.encode(), stored_hash)


def get_user_by_username(username: str, session: Session):
    """
    Retrieves a user from the database by their username.

    Args:
        username (str): The username of the user to retrieve.
        session (Session): The database session to use for the query.

    Returns:
        User: The user object corresponding to the provided username,
        or None if no user is found.
    """
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user


def create_user_in_db(username: str, password: str, session: Session):
    """
    Creates a new user in the database with the provided username and password.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        session (Session): The database session to use for the operation.

    Returns:
        User: The newly created user object.

    Raises:
        HTTPException: If there is an error creating the user in the database.
    """
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
    """
    Retrieves a user from the database by their username.

    Args:
        username (str): The username of the user to retrieve.
        session (Session): The database session to use for the query.

    Returns:
        User: The user object corresponding to the provided username,
        or None if no user is found.
    """
    user = get_user_by_username(username, session)
    if user is None:
        return None

    # verify user password
    if not verify_password(user.hashed_password, password):
        return None

    return user


def get_current_user(request: Request, session: Session = Depends(get_session)):
    """
    Verifies the provided token from the 'Authorization' cookie and
    returns the corresponding user.

    Args:
        request (Request): The incoming HTTP request.
        session (Session): The database session to use for the query.

    Returns:
        User: The user associated with the verified token.

    Raises:
        HTTPException: If the token is invalid or the user cannot be found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )
    token = request.cookies.get("Authorization")
    if not token:
        raise credentials_exception

    try:
        token = token.replace("Bearer ", "")

        payload = verify_token(token)

        if payload is None:
            raise credentials_exception
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(token_data.username, session)

    if user is None:
        raise credentials_exception
    return user

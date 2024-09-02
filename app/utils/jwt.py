from datetime import datetime, timedelta, timezone

from jose import jwt

from app.dependencies import get_settings

# from app.models.token import TokenData

ACCESS_TOKEN_EXPIRE_MINUTES = 30
settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.encryption_algo


def create_access_token(
    token_data: dict, expires_delta: timedelta | None = None
) -> str:
    data_to_encode = token_data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta

    # Store the expiration time as an integer
    data_to_encode.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    try:
        decoded_token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if the token has expired
        if decoded_token_data["exp"] < int(datetime.now(timezone.utc).timestamp()):
            return {"status": "expired"}  # Token has expired
        return {"status": "valid", "data": decoded_token_data}
    except jwt.ExpiredSignatureError:
        return {"status": "expired"}  # Explicit token expiry
    except jwt.JWTError:
        return None

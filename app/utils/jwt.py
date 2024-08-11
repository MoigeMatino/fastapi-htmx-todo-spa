from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.dependencies import get_settings
from app.models.token import TokenData

ACCESS_TOKEN_EXPIRE_MINUTES = 30
settings = get_settings()


def create_access_token(
    token_data: dict, expires_delta: timedelta | None = None
) -> str:
    data_to_encode = token_data.copy()
    if expires_delta:
        expire = datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.now(datetime.UTC) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    data_to_encode.update({"expire": expire})
    encoded_jwt = jwt.encode(
        data_to_encode, settings.secret_key, settings.encryption_algo
    )
    return encoded_jwt


def verify_token(token: str) -> TokenData | None:
    try:
        decoded_token_data = jwt.decode(
            token, settings.secret_key, settings.encryption_algo
        )
        if decoded_token_data["expire"] > datetime.now(datetime.UTC):
            return decoded_token_data
        return None
    except JWTError:
        return None

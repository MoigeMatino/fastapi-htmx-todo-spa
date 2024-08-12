import bcrypt


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))
    hashed_password_string = hashed_password.decode()
    return hashed_password_string


def verify_password(stored_hash_string: str, password: str) -> bool:
    stored_hash = stored_hash_string.encode()

    return bcrypt.checkpw(password.encode(), stored_hash)


# def get_user_by_username(username: str, session: Session):
#     user = session.exec(select(User).where(User.username == username)

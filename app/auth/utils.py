import bcrypt


def check_user_is_valid(user: dict) -> dict | tuple[str, str]:
    username = user.get("username", None)
    password = user.get("password", None)

    if (username is None) or (password is None):
        return {"Error": "username  or password is null"}

    return username, password


def hashed_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    password_hash = bcrypt.hashpw(password_bytes, salt)

    return password_hash


def check_hashed_password(password: str, hashed_password: bytes) -> bool:
    password_bytes = password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password)

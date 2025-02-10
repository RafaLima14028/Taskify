import bcrypt


def check_user_is_valid(user: dict) -> dict | tuple:
    username = user.get("username", None)
    email = user.get("email", None)
    password = user.get("password", None)

    if (username is None) or (email is None) or (password is None):
        return {"Error": "username, email or password is null"}

    return username, email, password


def hashed_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    password_hash = bcrypt.hashpw(password_bytes, salt)

    return password_hash


def check_hashed_password(password: str, hashed_password: bytes) -> bool:
    password_bytes = password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password)

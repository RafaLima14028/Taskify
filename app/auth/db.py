import psycopg2
from dotenv import load_dotenv
import os
import bcrypt

from app.utils import IncorrectPasswordError, NotFoundUserError


class DBAuth:
    def __init__(self):
        load_dotenv()

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = int(os.getenv("POSTGRES_PORT"))
        dbname = os.getenv("POSTGRES_DBNAME")

        try:
            self._conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                host=host,
                password=password,
                port=port,
            )
        except Exception:
            raise Exception("Cannot open auth db")
            self._conn = None

    def check_user(self, username: str, password: str) -> int:
        if not self._conn:
            raise Exception("The auth db is not open")

        cursor = self._conn.cursor()

        try:
            cursor.execute(
                """
                    SELECT id, hashed_password FROM users
                    WHERE username=%s;
                """,
                (username,),
            )

            result = cursor.fetchone()

            if result:
                user_id, hashed_password = result
                hashed_password = bytes(hashed_password)

                if self._check_hashed_password(password, hashed_password):
                    return user_id
                else:
                    raise IncorrectPasswordError
            else:
                raise NotFoundUserError
        except IncorrectPasswordError as e:
            raise IncorrectPasswordError
        except NotFoundUserError as e:
            raise NotFoundUserError
        except Exception as e:
            raise Exception(f"Unable to query authentication db: {e}")
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def _check_hashed_password(password: str, hashed_password: bytes) -> bool:
        password_bytes = password.encode("utf-8")

        return bcrypt.checkpw(password_bytes, hashed_password)

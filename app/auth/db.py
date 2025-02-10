import psycopg2
from dotenv import load_dotenv
import os

from app.auth.utils import check_hashed_password


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
                dbname="taskifyDB",
                user="postgres",
                host="localhost",
                password="1234",
                port=5432,
            )
        except Exception:
            raise Exception("Cannot open auth db")
            self._conn = None

    def check_user(self, username: str, password: str) -> dict:
        if not self._conn:
            raise Exception("Error: The auth db is not open")

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

                if check_hashed_password(password, hashed_password):
                    return {"ID": user_id}
                else:
                    return {"Error": "Incorrect password"}
            else:
                return {"Not Found": "User not exists in database"}
        except Exception as e:
            raise Exception(f"Unable to query authentication db: {e}")
        finally:
            if cursor:
                cursor.close()

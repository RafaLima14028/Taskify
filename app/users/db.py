import psycopg2
from dotenv import load_dotenv
import os

from app.utils import UsernameOrEmailAlreadyBeenCreatedError


class DBUsers:
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
            raise Exception("Cannot open users db")
            self._conn = None

        self._create_table()

    def _create_table(self) -> None:
        if not self._conn:
            raise Exception("Cannot open users db")

        cursor = self._conn.cursor()

        try:
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        hashed_password BYTEA NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """
            )

            self._conn.commit()
        except Exception as e:
            raise Exception(f"Cannot create table users: {e}")
        finally:
            if cursor:
                cursor.close()

    def close(self) -> None:
        if self._conn:
            self._conn.close()

    def create_user(self, username: str, email: str, hashed_password: bytes) -> None:
        if not self._conn:
            raise Exception("Cannot open users db")

        cursor = self._conn.cursor()

        try:
            cursor.execute(
                """
                    INSERT INTO users (username, email, hashed_password)
                    VALUES (%s, %s, %s);
                """,
                (username, email, hashed_password),
            )

            self._conn.commit()
        except psycopg2.errors.UniqueViolation:
            raise UsernameOrEmailAlreadyBeenCreatedError
        except Exception:
            raise Exception("Cannot create user")
        finally:
            if cursor:
                cursor.close()

    def update_user(
        self, user_id: int, username: str, email: str, hashed_password: bytes
    ) -> None:
        if not self._conn:
            raise Exception("Cannot open users db")

        cursor = self._conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET hashed_password = %s WHERE id = %s AND username = %s AND email = %s;",
                (hashed_password, user_id, username, email),
            )

            self._conn.commit()
        except Exception as e:
            raise Exception("Cannot update user")
        finally:
            if cursor:
                cursor.close()

    def delete_user(self, user_id: int) -> None:
        if not self._conn:
            raise Exception("Cannot open users db")

        cursor = self._conn.cursor()

        try:
            cursor.execute(
                "DELETE FROM users WHERE id = %s;",
                (user_id,),
            )

            self._conn.commit()
        except Exception as e:
            raise Exception("Cannot delete user")
        finally:
            if cursor:
                cursor.close()

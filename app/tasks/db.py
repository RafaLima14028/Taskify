import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime


class DBTasks:
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
            raise Exception("Error: Cannot open tasks db")
            self._conn = None

        self._create_table()

    def _create_table(self) -> None:
        if not self._conn:
            raise Exception("Error: The tasks db is not open")

        cursor = self._conn.cursor()

        try:
            cursor.execute(
                """
                        CREATE TABLE IF NOT EXISTS tasks (
                            id SERIAL PRIMARY KEY,
                            title TEXT NOT NULL,
                            content TEXT,
                            status TEXT DEFAULT 'pending',
                            priority INTEGER DEFAULT 1,
                            due_date DATE,
                            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_edition TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """
            )

            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM pg_proc
                    WHERE proname = 'update_last_edition'
                );
                """
            )
            function_exists = cursor.fetchone()[0]

            if not function_exists:
                cursor.execute(
                    """
                    CREATE FUNCTION update_last_edition()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.last_edition = CURRENT_TIMESTAMP;
                        RETURN NEW;
                    END;
                    $$ LANGUAGE plpgsql;
                    """
                )

            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM pg_trigger
                    WHERE tgname = 'trigger_update_last_edition'
                );
                """
            )
            trigger_exists = cursor.fetchone()[0]

            if not trigger_exists:
                cursor.execute(
                    """
                    CREATE TRIGGER trigger_update_last_edition
                    BEFORE UPDATE ON tasks
                    FOR EACH ROW
                    EXECUTE FUNCTION update_last_edition();
                    """
                )

            self._conn.commit()
        except Exception:
            raise Exception("Error: Cannot create table, function or trigger tasks")
        finally:
            if cursor:
                cursor.close()

    def close(self) -> None:
        if self._conn:
            self._conn.close()

    def create_task(
        self,
        title: str,
        content: str = None,
        status: str = None,
        priority: str = None,
        due_date: str = None,
    ) -> None:
        priority = int(priority) if priority and priority.isdigit() else 1

        if due_date:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

        if not self._conn:
            raise Exception("Error: The tasks db is not open")

        cursor = self._conn.cursor()

        columns, values = self._prepare_update_query_data(
            title, content, status, priority, due_date
        )

        try:
            cursor.execute(
                f"""
                    INSERT INTO tasks ({', '.join(columns)})
                    VALUES ({', '.join(['%s'] * len(values))});
                """,
                values,
            )

            self._conn.commit()
        except Exception:
            raise Exception("Error: Cannot create the task")
        finally:
            if cursor:
                cursor.close()

    def get_tasks(self) -> dict:
        if not self._conn:
            raise Exception("Error: The tasks db is not open")

        cursor = self._conn.cursor()
        tasks = dict()

        try:
            cursor.execute(
                """
                    SELECT * FROM tasks;
                """
            )

            rows = cursor.fetchall()

            for i in rows:
                tasks[i[0]] = {
                    "title": i[1],
                    "content": i[2],
                    "status": i[3],
                    "priority": i[4],
                    "due_date": str(i[5]),
                    "created": i[6].strftime("%Y-%m-%d"),
                    "last_edition": i[7].strftime("%Y-%m-%d"),
                }
        except Exception:
            raise Exception("Error: Cannot get the tasks")
        finally:
            if cursor:
                cursor.close()

        return tasks

    def update_tasks(
        self,
        task_id: int,
        title: str,
        content: str = None,
        status: str = None,
        priority: str = None,
        due_date: str = None,
    ):
        if not self._conn:
            raise Exception("Error: The tasks db is not open")

        cursor = self._conn.cursor()

        priority = int(priority) if priority and priority.isdigit() else 1

        if due_date:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

        columns, values = self._prepare_update_query_data(
            title, content, status, priority, due_date
        )
        values.append(task_id)

        query = (
            "UPDATE tasks SET "
            + ", ".join(f"{col}=%s" for col in columns)
            + f" WHERE id=%s;"
        )

        try:
            cursor.execute(query, values)

            self._conn.commit()
        except Exception:
            raise Exception("Error: Cannot update the tasks")
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def _prepare_update_query_data(
        title: str,
        content: str = None,
        status: str = None,
        priority: int = None,
        due_date: datetime = None,
    ) -> tuple[list, tuple]:
        columns = ["title"]
        values = [title]

        if content is not None:
            columns.append("content")
            values.append(content)

        if status is not None:
            columns.append("status")
            values.append(status)

        if priority is not None:
            columns.append("priority")
            values.append(priority)

        if due_date is not None:
            columns.append("due_date")
            values.append(due_date)

        return columns, values

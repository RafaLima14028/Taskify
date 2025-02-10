def check_task_is_valid(task: dict) -> dict | tuple:
    title = task.get("title", None)

    if not title:
        return {"Error": f"The task has no title"}

    content = task.get("content", None)
    status = task.get("status", None)
    priority = task.get("priority", None)
    due_date = task.get("due_date", None)

    return title, content, status, priority, due_date

<h1 aling="center">Taskify</h1>

An API for task management built with FastAPI. It includes operations for creating, listing, and managing tasks with a modular structure and support for future expansion. This project serves as a portfolio example and demonstrates best practices in API development.

## Technologies Used:

- [Python](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Git](https://git-scm.com/)

## Libraries Python Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Psycopg2](https://www.psycopg.org/docs/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Bcrypt](https://pypi.org/project/bcrypt/)
- [PyJWT](https://github.com/jpadilla/pyjwt)

## Running the project:

Follow the steps below to set up and run the project locally:

1. **Clone the respository**:

   ```bash
   git clone https://github.com/RafaLima14028/Taskify.git
   cd Taskify
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   - **Linux/Mac**:

     ```bash
     source .venv/bin/activate
     ```

   - **Windows**:

     ```bash
     .\.venv\Scripts\activate
     ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

### Observation

You may need to change the port for uvicorn if the default port is already in use.

## Project Structure:

```bash
├───.venv
├───app
│   ├───auth
│   │   ├─ db.py
│   │   └─ routes.py
│   ├───tasks
│   │   ├─ db.py
│   │   └─ routes.py
│   ├───users
│   │   ├─ db.py
│   │   └─ routes.py
│   └─ utils.py
├─── .env
├─── .gitignore
├─── main.py
├─── README.md
└─── requirements.txt
```

## Routes:

### User management:

- **Create a user** (`POST /users`):  
  Create a new user in the database.
- **Update a user's password** (`PUT /users`):  
  Updates the password of an existing user.
- **Delete a user** (`DELETE /users`):  
  Deletes a user from the database.

### **Task Management**

- **List all tasks** (`GET /tasks`):  
  Retrieves all tasks associated with the authenticated user.
- **Create a task** (`POST /tasks`):  
  Creates a new task for the authenticated user.
- **Update a task** (`PUT /tasks/{task_id}`):  
  Updates the details of an existing task.

### **Authentication**

- **User authentication** (`POST /auth`):  
  Authenticates a user and returns a JWT token.

## Request Details:

### Body Examples:

Specify the JSON structure for each request's body.

- **Create User (`/users`)**:

  ```JSON
  {
     "username": "user1",
     "email": "user1.test@exemple.com",
     "password": "12345"
  }
  ```

- **Update Password (`/users`)**:

  ```JSON
  {
     "username": "user1",
     "email": "user1.test@exemple.com",
     "password": "54321"
  }
  ```

- **Delete User (`/users`)**: No body.

- **Create Task (`/tasks`)**:

  ```JSON
  {
     "title": "Go to the supermarket",
     "content": "Buy milk, bread, bananas and rice",
     "status": "Complet",
     "priority": 2,
     "due_date": "2025-02-22"
  }
  ```

- **Update Task (`/tasks/{task_id}`)**:

  ```JSON
  {
     "title": "Go to the supermarket",
     "status": "Pending",
     "priority": 3,
     "due_date": "2025-02-25"
  }
  ```

- **User Authentication (`/auth`)**:

  ```JSON
  {
     "username": "user1",
     "password": "54321"
  }
  ```

## Headers:

Specify the required headers for the API routes.

- **Authentication Header:**

```Header
Authorization: Bearer <JWT_TOKEN>
```

This header is required for routes that need user authentication, such as `PUT /users`, `DELETE /users`, `GET /tasks`, `POST /tasks` and `PUT /tasks/{task_id}`.

## About database:

![Database model](img_readme/db-model.png)

## About .env:

In the .env file there are some environment variables for the database and JWT (JSON Web Token).

```bash
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "1234"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DBNAME = "taskifyDB"

JWT_SECRET_KEY = "Taskify"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTE = 30
```

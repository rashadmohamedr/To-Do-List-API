Here is the same **README.md**, clean and professional, with **no emojis**.

---

# To-Do List API (FastAPI + JWT Authentication)

A simple, clean, educational REST API built with FastAPI, featuring:

* User registration and login
* JWT Authentication
* Protected `/auth/me` route
* CRUD operations for tasks
* Automatic OpenAPI (Swagger) documentation
* SQLite database with SQLAlchemy ORM

---

## Features

### Authentication

* Signup new users
* Login returns a JWT access token
* Get current user via `Authorization: Bearer <token>`

### Tasks API

* Create tasks
* List tasks
* Toggle task completion
* Delete tasks

---

## Project Structure

```
project/
│── main.py
│── database.py
│── models.py
│── schemas.py
│── routers/
│   ├── auth.py
│   └── tasks.py
│── services/
│   └── auth_service.py
│── app
│   ├──core
│   |   ├── __init__.py
│   |   ├── config.py
│   |   ├── jwt.py
│   |   └── security.py
│   ├──db
│   |   ├── __init__.py
│   |   └── database.py
│   ├──internal
│   |   └── admin.py #not used for now
│   ├──models
│   |   ├── __init__.py
│   |   ├── task.py
│   |   └── user.py
│   ├──routers
│   |   ├── __init__.py
│   |   ├── auth.py
│   |   └── tasks.py
│   ├──schemas
│   |   ├── __init__.py
│   |   ├── task.py
│   |   └── user.py
│   └──services
│       ├── __init__.py
│       ├── auth_service.py
│       └── task_service.py
│── requirements.txt
│── README.md
│── docker-compose.yml
└── .env
```

---

## Installation and Setup

### 1. Clone the project

```bash
git clone <your-repo-url>
cd project
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux & Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI server

```bash
uvicorn main:app --reload
```

### 5. Open the API documentation

Swagger UI:

```
http://localhost:8000/docs
```

OpenAPI JSON:

```
http://localhost:8000/openapi.json
```

---

## Authentication Endpoints

### POST /auth/signup

Register a new user.

Request:

```json
{
  "email": "user@example.com",
  "password": "string",
  "username": "string"
}
```

Response:

```json
"Account created successfully"
```

---

### POST /auth/login

Authenticate and receive a JWT access token.

Request:

```json
{
  "email": "user@example.com",
  "password": "string"
}
```

Response:

```json
{
  "message": "Welcome back, username!",
  "token": "<JWT_TOKEN>"
}
```

---

### GET /auth/me

Requires an Authorization header:

```
Authorization: Bearer <token>
```

Response:

```json
{
  "email": "user@example.com"
}
```

---

## Tasks Endpoints

### GET /tasks/Tasks/

List all tasks.

Response:

```json
[
  {
    "title": "Buy milk",
    "description": "2 liters",
    "id": 1,
    "completed": false
  }
]
```

---

### POST /tasks/Tasks/

Create a new task.

Request:

```json
{
  "title": "Study FastAPI",
  "description": "JWT + CRUD example"
}
```

---

### POST /tasks/Tasks/{task_title}/toggle

Toggle the completion status of a specific task.

Response:

```json
"Task toggled"
```

---

### DELETE /tasks/Tasks/{task_title}

Delete a task by title.

---

## Database

* Uses SQLite
* Tables are created automatically
* Managed by SQLAlchemy ORM

---

## JWT Details

JWT tokens include:

```json
{
  "sub": "<user_id>",
  "username": "<username>",
  "exp": "<expiry_timestamp>"
}
```

Protected routes use FastAPI dependency injection to validate the token.

---

## Testing

You can test all endpoints in Swagger UI.

Example cURL test:

```bash
curl -X GET \
  http://127.0.0.1:8000/auth/me \
  -H "Authorization: Bearer <your_token>"
```

---

## License

MIT License (or specify your preferred license)



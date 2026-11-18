# ✅ FastAPI ToDo App

A full-stack todo app: a **FastAPI** REST backend with **PostgreSQL** persistence via **SQLAlchemy**, optional **file attachments**, and a **Streamlit** frontend that talks to the API.

## Features

- **CRUD API** for todos: create, list, get one, update, delete one, delete all
- **Filter by status:** `GET /todos?completed=true|false`
- **File attachments:** attach an image or file to a todo, replace it, or remove it. Files are saved with unique names and served from `/uploads`
- **Automatic timestamps:** `created_at` and `updated_at` on every todo
- **Input validation** with Pydantic and clear `404` / `400` errors
- **Streamlit UI:** dashboard metrics (total / completed / pending), add and edit forms, status filter, inline image previews

## Tech stack

`Python` · `FastAPI` · `SQLAlchemy 2.0` · `PostgreSQL` (psycopg 3) · `Pydantic` · `Streamlit` · `Requests`

## Project structure

```
todo_app.py      FastAPI app: routes, file handling, DB session dependency
database.py      SQLAlchemy engine and session (reads DATABASE_URL from .env)
models.py        TodoModel table definition
frontend.py      Streamlit frontend that calls the API
.env.example     Template for your local settings
```

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Health check |
| `POST` | `/todos` | Create a todo (form fields: `title`, optional `file`) |
| `GET` | `/todos` | List todos, optionally filtered by `completed` |
| `GET` | `/todos/{id}` | Get one todo |
| `PUT` | `/todos/{id}` | Update `title`, `completed`, replace `file`, or `remove_file` |
| `DELETE` | `/todos/{id}` | Delete a todo and its attachment |
| `DELETE` | `/todos` | Delete all todos |

Interactive docs are available at `http://127.0.0.1:8000/docs` once the API is running.

## Getting started

**1. Clone and install**

```bash
git clone https://github.com/Amanathussain205/fast-api-todo-app.git
cd fast-api-todo-app
python -m venv .venv
.venv\Scripts\activate          # Windows; use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
```

**2. Configure the database**

Create a PostgreSQL database (for example `todo_db`), then:

```bash
cp .env.example .env            # Windows: copy .env.example .env
```

Edit `.env` and set `DATABASE_URL` to your own connection string. The `todos` table is created automatically the first time the API starts.

**3. Run the API**

```bash
uvicorn todo_app:app --reload
```

**4. Run the frontend** (in a second terminal)

```bash
streamlit run frontend.py
```

## What I learned

- Structuring a FastAPI project with a database session dependency (`Depends(get_db)`)
- Modelling tables with SQLAlchemy 2.0 typed mappings
- Handling multipart form data and file uploads safely (unique filenames, cleanup on replace/delete)
- Connecting a Streamlit frontend to a REST API

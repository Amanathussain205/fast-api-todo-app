# 📝 Todo App — FastAPI, PostgreSQL & Streamlit

A full-stack **Todo Management Application** built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **Streamlit**.

The project started as a simple Todo application using in-memory Python data and was progressively upgraded into a database-backed application with persistent storage, complete CRUD operations, database migrations, file-upload support, timestamps, a browser-accessible file system, and a separate Streamlit frontend.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Application Architecture](#-application-architecture)
- [Project Structure](#-project-structure)
- [How the Application Works](#-how-the-application-works)
- [Todo Data Model](#-todo-data-model)
- [CRUD Operations](#-crud-operations)
- [PostgreSQL Integration](#-postgresql-integration)
- [SQLAlchemy](#-sqlalchemy)
- [Alembic Database Migrations](#-alembic-database-migrations)
- [File Upload System](#-file-upload-system)
- [Static File Access](#-static-file-access)
- [Automatic Timestamps](#-automatic-timestamps)
- [FastAPI Documentation](#-fastapi-documentation)
- [Streamlit Frontend](#-streamlit-frontend)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Database Configuration](#-database-configuration)
- [Alembic Workflow](#-alembic-workflow)
- [API Endpoints](#-api-endpoints)
- [Example Workflow](#-example-workflow)
- [Git & GitHub](#-git--github)
- [Important Concepts Learned](#-important-concepts-learned)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

# 🚀 Project Overview

This project is a **full-stack Todo management system** designed to demonstrate how a modern Python web application can be developed step by step.

The application provides an API through **FastAPI** and stores Todo information persistently in **PostgreSQL**.

Instead of keeping Todo data temporarily inside Python memory, the application uses:

```text
Streamlit Frontend
       ↓
    FastAPI
       ↓
   SQLAlchemy
       ↓
   PostgreSQL
```

**Alembic** is used alongside SQLAlchemy to manage changes to the database schema over time.

The application also supports uploading files and storing their relative paths in the database rather than storing the actual file binary inside PostgreSQL.

---

# ✨ Key Features

## Todo Management

- ✅ Create Todos
- ✅ Read Todos
- ✅ Read an individual Todo
- ✅ Update Todos
- ✅ Delete Todos
- ✅ Mark Todos as completed/incomplete
- ✅ Assign Todo priority
- ✅ Validate request data using Pydantic

## Database

- ✅ PostgreSQL database
- ✅ SQLAlchemy ORM
- ✅ Persistent Todo storage
- ✅ Structured database models
- ✅ Database sessions
- ✅ Database schema management

## Database Migrations

- ✅ Alembic integration
- ✅ Migration generation
- ✅ Migration upgrades
- ✅ Migration downgrades
- ✅ Schema version tracking

## File Handling

- ✅ Upload files through FastAPI
- ✅ Receive uploaded files using `UploadFile`
- ✅ Detect uploaded file type using `content_type`
- ✅ Store uploaded files inside an application-controlled `uploads` directory
- ✅ Store the relative file path in PostgreSQL
- ✅ Serve uploaded files through FastAPI
- ✅ Access uploaded files through browser URLs

## Application Metadata

- ✅ `created_at` timestamp
- ✅ `updated_at` timestamp

## API Development

- ✅ REST-style API endpoints
- ✅ HTTP status codes
- ✅ Request validation
- ✅ Response models
- ✅ Error handling
- ✅ Swagger UI
- ✅ ReDoc

## Frontend

- ✅ Separate Streamlit frontend
- ✅ Communicates with the FastAPI backend
- ✅ Provides a user-friendly interface for interacting with Todos

---

# 🛠 Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **FastAPI** | Backend API framework |
| **Pydantic** | Data validation and schemas |
| **PostgreSQL** | Relational database |
| **SQLAlchemy** | Python ORM and database interaction |
| **psycopg** | PostgreSQL database driver |
| **Alembic** | Database migration management |
| **Streamlit** | Frontend/UI |
| **Uvicorn** | ASGI server |
| **Swagger UI** | Interactive API documentation |
| **ReDoc** | Alternative API documentation |
| **Git** | Version control |
| **GitHub** | Remote source-code repository |

---

# 🏗 Application Architecture

The application follows a layered architecture.

```text
                 ┌──────────────────────┐
                 │   Streamlit Frontend │
                 │      frontend.py     │
                 └──────────┬───────────┘
                            │
                            │ HTTP Requests
                            ▼
                 ┌──────────────────────┐
                 │       FastAPI        │
                 │    todo_app.py       │
                 └──────────┬───────────┘
                            │
                            │ ORM Operations
                            ▼
                 ┌──────────────────────┐
                 │      SQLAlchemy      │
                 │       models.py      │
                 └──────────┬───────────┘
                            │
                            │ SQL
                            ▼
                 ┌──────────────────────┐
                 │     PostgreSQL       │
                 │      Database        │
                 └──────────────────────┘

                 ┌──────────────────────┐
                 │       Alembic        │
                 │ Database Migrations  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     PostgreSQL       │
                 │   Schema Changes     │
                 └──────────────────────┘
```

---

# 📂 Project Structure

A simplified representation of the project is:

```text
Todo-App/
│
├── todo_app.py
├── frontend.py
├── models.py
├── database.py
│
├── uploads/
│   └── uploaded files
│
├── alembic/
│   ├── versions/
│   │   └── migration files
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
├── requirements.txt
└── README.md
```

### Main Files

### `todo_app.py`

The main FastAPI backend.

Responsible for:

- Creating the FastAPI application
- Defining API routes
- Handling Todo operations
- Handling file uploads
- Returning responses
- Serving uploaded files
- Connecting the API logic with the database

### `models.py`

Contains the SQLAlchemy database models.

The Todo model represents the Todo table in PostgreSQL.

### `database.py`

Responsible for database configuration.

It contains the components required for SQLAlchemy to communicate with PostgreSQL, including:

- Database URL
- SQLAlchemy engine
- Session factory
- Database session configuration
- Declarative base

### `frontend.py`

Contains the Streamlit frontend.

It communicates with the FastAPI backend and provides the user interface through which users can interact with the Todo application.

### `alembic/`

Contains Alembic's migration environment and migration versions.

### `uploads/`

Application-controlled directory where uploaded files are stored.

---

# 📊 Todo Data Model

The Todo database model contains fields such as:

| Field | Purpose |
|---|---|
| `id` | Unique identifier for each Todo |
| `title` | Todo title |
| `completed` | Completion status |
| `priority` | Todo priority |
| `file_path` | Relative path of an uploaded file |
| `created_at` | Creation timestamp |
| `updated_at` | Last-update timestamp |

Conceptually, a Todo record looks like:

```text
Todo
│
├── id
├── title
├── completed
├── priority
├── file_path
├── created_at
└── updated_at
```

---

# 🔄 CRUD Operations

CRUD stands for:

```text
C → Create
R → Read
U → Update
D → Delete
```

These four operations form the foundation of the Todo application's database functionality.

---

## 1. Create

A client sends Todo information to the FastAPI backend.

```text
Frontend
   ↓
POST request
   ↓
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

The Todo is inserted into the database and receives a unique ID.

---

## 2. Read

The application can retrieve:

- All Todos
- A specific Todo

The backend queries PostgreSQL through SQLAlchemy and returns the result.

---

## 3. Update

An existing Todo can be modified.

For example:

```text
title
completed
priority
file information
```

After modification, the `updated_at` value can reflect the latest change.

---

## 4. Delete

A Todo can be removed from PostgreSQL.

```text
DELETE request
       ↓
FastAPI
       ↓
SQLAlchemy
       ↓
PostgreSQL
       ↓
Todo removed
```

---

# 🐘 PostgreSQL Integration

Originally, Todo information could be stored directly inside Python memory.

For example:

```text
Python Application
       ↓
Python Dictionary/List
```

This approach is unsuitable for a real application because the data disappears when the application stops.

The application was therefore upgraded to:

```text
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

PostgreSQL provides **persistent storage**, meaning Todo information remains available after the application restarts.

---

# 🔌 SQLAlchemy

SQLAlchemy is the ORM used by the application.

ORM stands for:

> **Object-Relational Mapping**

It allows Python code to work with database tables using Python objects and classes.

Conceptually:

```text
Python Object
     ↓
SQLAlchemy ORM
     ↓
SQL
     ↓
PostgreSQL
```

Instead of manually writing SQL for every operation, the application can use SQLAlchemy models and database sessions.

---

# 🧩 SQLAlchemy Components

## Engine

The SQLAlchemy engine establishes the application's connection mechanism to PostgreSQL.

```text
FastAPI
   ↓
Engine
   ↓
PostgreSQL
```

---

## Session

A SQLAlchemy session represents the application's interaction with the database.

It can be used to:

- Query records
- Add records
- Modify records
- Delete records
- Commit transactions

---

## Session Factory

A session factory is used to create database sessions whenever the application needs to interact with PostgreSQL.

---

## Model

A SQLAlchemy model represents a database table.

For example:

```text
Python Class
     ↓
SQLAlchemy Model
     ↓
PostgreSQL Table
```

The Todo model therefore acts as the Python representation of the Todo table.

---

# 🛠 Alembic Database Migrations

Alembic is used to manage **database schema changes**.

This became especially important as the Todo application evolved.

For example, suppose the original table contained:

```text
id
title
completed
priority
```

Later, the application required:

```text
file_path
created_at
updated_at
```

Simply changing the Python model does not automatically mean the existing PostgreSQL table has been updated correctly.

Alembic bridges this gap.

```text
Change SQLAlchemy Model
          ↓
Create Alembic Migration
          ↓
Run Migration
          ↓
PostgreSQL Schema Updated
```

---

# 🔁 Alembic Workflow

A typical migration workflow is:

```text
1. Change SQLAlchemy model
            ↓
2. Generate migration
            ↓
3. Review migration
            ↓
4. Upgrade database
            ↓
5. PostgreSQL schema changes
```

To move the database forward:

```bash
alembic upgrade head
```

To move the database backward by one migration:

```bash
alembic downgrade -1
```

Alembic therefore provides a controlled history of database schema changes.

---

# 📁 File Upload System

The application also supports file uploads.

FastAPI provides `UploadFile` for receiving uploaded files.

The upload process can be understood as:

```text
User
 ↓
Select File
 ↓
Frontend / HTTP Request
 ↓
FastAPI
 ↓
UploadFile
 ↓
uploads/ directory
 ↓
Relative file path stored in PostgreSQL
```

---

# 🔐 File Storage Design

The application does **not** need to store the actual file binary inside the Todo database.

Instead, the uploaded file is saved inside the application's `uploads` directory.

The database stores information such as:

```text
uploads/example.pdf
```

rather than relying on the user's original computer path.

This separates:

- **File storage**
- **Database metadata**

The database therefore knows where the application's copy of the file is located without depending on a user's local filesystem path.

---

# 🌐 Static File Access

FastAPI can expose the application's `uploads` directory through a static route.

This allows uploaded files to be accessed through a browser.

For example, an uploaded file may become accessible through a URL similar to:

```text
http://127.0.0.1:8000/uploads/example.pdf
```

The overall flow is:

```text
PostgreSQL
    │
    │ stores relative file path
    ▼
uploads/
    │
    │ contains actual file
    ▼
FastAPI StaticFiles
    │
    ▼
Browser URL
```

This makes the uploaded resource accessible without storing the actual file content in PostgreSQL.

---

# ⏰ Automatic Timestamps

The Todo records also support timestamp information.

## `created_at`

Records when the Todo was created.

## `updated_at`

Records when the Todo was last updated.

Conceptually:

```text
Todo Created
     ↓
created_at = current time
     ↓
Todo Updated
     ↓
updated_at = latest update time
```

These timestamps are useful for tracking the lifecycle of database records.

They also demonstrate how application-level changes, SQLAlchemy models, Alembic migrations, and PostgreSQL work together.

---

# 📚 FastAPI Documentation

FastAPI automatically generates interactive API documentation.

Once the backend is running, Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

ReDoc is available at:

```text
http://127.0.0.1:8000/redoc
```

Swagger UI allows developers to:

- View available endpoints
- Inspect request parameters
- Inspect request bodies
- Execute API requests
- Upload files
- View API responses
- Test the backend without building a frontend first

---

# 🖥 Streamlit Frontend

The project contains a separate Streamlit frontend.

The frontend acts as the user-facing layer.

Instead of directly interacting with PostgreSQL, the frontend communicates with FastAPI.

```text
User
 ↓
Streamlit
 ↓
HTTP Request
 ↓
FastAPI
 ↓
SQLAlchemy
 ↓
PostgreSQL
```

This separation is important because the frontend does not need to know how the database works internally.

---

# 🔗 Frontend–Backend Communication

The application follows a client-server architecture.

### Frontend

Responsible for:

- User interaction
- Input collection
- Displaying Todos
- Sending requests
- Displaying responses

### Backend

Responsible for:

- API routes
- Validation
- Business logic
- Database interaction
- File handling
- Error handling

### Database

Responsible for:

- Persistent data storage
- Todo records
- File metadata
- Timestamps

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd <project-directory>
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

The project requires the major packages used by the application, including FastAPI, Uvicorn, SQLAlchemy, PostgreSQL's Python driver, Alembic, and Streamlit.

---

# 🐘 Database Configuration

PostgreSQL must be installed and running before starting the application.

The application uses a database connection string commonly represented as:

```text
DATABASE_URL
```

Conceptually, it contains:

```text
database dialect
+
database driver
+
username
+
password
+
host
+
port
+
database name
```

For example, the structure is:

```text
postgresql+psycopg://USERNAME:PASSWORD@HOST:PORT/DATABASE
```

The actual credentials should be configured locally and **must not be committed to GitHub**.

---

# 🔒 Environment Variables

Sensitive configuration such as database credentials should ideally be stored in environment variables or a local `.env` file.

Example:

```text
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/todo_db
```

A real password should never be hard-coded into publicly shared source code.

---

# 🗃️ Initialize the Database

After PostgreSQL has been configured, Alembic can be used to bring the database schema up to date:

```bash
alembic upgrade head
```

This applies all available migrations.

---

# ▶️ Running the Backend

Start the FastAPI application with Uvicorn:

```bash
uvicorn todo_app:app --reload
```

The backend will normally become available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ▶️ Running the Frontend

Start the Streamlit frontend with:

```bash
streamlit run frontend.py
```

Streamlit will provide a local browser URL through which the frontend can be accessed.

The frontend then communicates with the running FastAPI backend.

---

# 🔄 Complete Application Workflow

The complete application can be visualized as:

```text
                    USER
                      │
                      ▼
             ┌─────────────────┐
             │    Streamlit    │
             │    Frontend     │
             └────────┬────────┘
                      │
                  HTTP Request
                      │
                      ▼
             ┌─────────────────┐
             │     FastAPI     │
             │     Backend     │
             └────────┬────────┘
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
      ┌─────────────┐   ┌──────────────┐
      │  SQLAlchemy │   │ File Handler │
      └──────┬──────┘   └──────┬───────┘
             │                 │
             ▼                 ▼
      ┌─────────────┐   ┌──────────────┐
      │ PostgreSQL  │   │   uploads/   │
      └─────────────┘   └──────────────┘
```

Alembic operates alongside the database layer:

```text
SQLAlchemy Model
       ↓
Alembic Migration
       ↓
PostgreSQL Schema
```

---

# 🔌 API Endpoints

The backend exposes endpoints for the major Todo operations.

A typical REST structure is:

| HTTP Method | Purpose |
|---|---|
| `POST` | Create a Todo |
| `GET` | Retrieve Todos |
| `GET` | Retrieve a specific Todo |
| `PUT` / `PATCH` | Update a Todo |
| `DELETE` | Delete a Todo |
| `POST` | Upload a file |

The exact request and response schemas are documented automatically in Swagger UI.

---

# 🧪 Example API Lifecycle

Consider creating a Todo:

```text
User enters:
"Learn FastAPI"
```

The request reaches:

```text
Streamlit
    ↓
FastAPI
    ↓
Pydantic Validation
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

PostgreSQL stores the Todo.

Later, when the user requests the Todos:

```text
Streamlit
    ↓
GET request
    ↓
FastAPI
    ↓
SQLAlchemy
    ↓
PostgreSQL
    ↓
FastAPI Response
    ↓
Streamlit
```

The frontend displays the stored Todo.

---

# 📎 Example File Upload Lifecycle

When a user uploads a file:

```text
User selects file
       ↓
Streamlit / HTTP request
       ↓
FastAPI UploadFile
       ↓
Application saves file
       ↓
uploads/example.pdf
       ↓
Relative path saved in PostgreSQL
       ↓
Browser can access the file through FastAPI
```

This keeps the actual file in the filesystem while the database stores its application-level location.

---

# 🧠 Important Concepts Learned

This project demonstrates several important backend and AI-engineering-adjacent software engineering concepts.

## FastAPI

A modern Python framework for building APIs.

## REST API

A structured way for applications to communicate over HTTP.

## Pydantic

Used to validate and structure incoming and outgoing data.

## HTTP Methods

```text
POST   → Create
GET    → Read
PUT    → Update
PATCH  → Partial Update
DELETE → Delete
```

## PostgreSQL

A relational database used for persistent application data.

## SQLAlchemy

An ORM that allows Python applications to interact with relational databases.

## Database Session

A controlled interaction with the database for querying and modifying records.

## Alembic

A migration tool used to keep database schemas synchronized with evolving application models.

## UploadFile

FastAPI's mechanism for receiving uploaded files.

## StaticFiles

Allows files stored by the application to be served through HTTP.

## Swagger UI

An interactive interface for testing and understanding APIs.

## Streamlit

A Python framework used here to build the frontend.

---

# 🧩 Why the Project Was Progressively Upgraded

The project demonstrates a realistic progression from a simple Python application toward a more production-oriented architecture.

### Stage 1 — In-Memory Application

```text
FastAPI
  ↓
Python Dictionary
```

Simple, but data is temporary.

### Stage 2 — PostgreSQL

```text
FastAPI
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

Data becomes persistent.

### Stage 3 — Alembic

```text
SQLAlchemy Models
       ↓
    Alembic
       ↓
PostgreSQL Schema
```

Database changes become manageable and version-controlled.

### Stage 4 — File Handling

```text
FastAPI
  ├── PostgreSQL → file metadata
  └── uploads/   → actual files
```

The application can now work with uploaded files.

### Stage 5 — Metadata

```text
created_at
updated_at
```

The application can track record creation and modification.

### Stage 6 — Frontend

```text
Streamlit
    ↓
FastAPI
    ↓
PostgreSQL
```

The backend becomes accessible through a dedicated user interface.

---

# 🌿 Git & GitHub

Git is used for version control, while GitHub provides remote repository hosting.

The project can be maintained through branches such as:

```text
main
feature-updates
```

A feature branch allows changes to be developed separately from the main branch.

Typical workflow:

```text
main
  │
  └── feature-updates
          │
          ├── Develop changes
          ├── Test changes
          └── Commit changes
                  │
                  ▼
               Merge
                  │
                  ▼
                main
```

Useful Git commands include:

```bash
git status
git add .
git commit -m "Your commit message"
git push
git pull
git branch
git switch main
git switch feature-updates
git merge feature-updates
```

---

# 🔐 Security Considerations

When deploying or sharing the application, several security practices should be followed.

### Database Credentials

Never commit real database passwords to GitHub.

### Environment Variables

Use environment variables for sensitive configuration.

### Uploaded Files

Uploaded files should be validated appropriately before being accepted.

### File Paths

The application should use controlled application paths rather than trusting arbitrary paths supplied by clients.

### Production Deployment

Development settings such as:

```bash
--reload
```

should generally not be used as the production deployment strategy.

---

# 🧪 Testing the Application

Swagger UI provides a convenient way to test backend functionality before interacting with the Streamlit frontend.

Recommended testing order:

```text
1. Start PostgreSQL
        ↓
2. Run Alembic migrations
        ↓
3. Start FastAPI
        ↓
4. Open /docs
        ↓
5. Test CRUD endpoints
        ↓
6. Test file upload
        ↓
7. Verify PostgreSQL records
        ↓
8. Start Streamlit
        ↓
9. Test complete frontend workflow
```

---

# 🐛 Troubleshooting

## FastAPI does not start

Check:

- Virtual environment activation
- Installed dependencies
- Correct module name
- Correct FastAPI application variable
- PostgreSQL availability

---

## Database connection fails

Check:

- PostgreSQL service is running
- Database exists
- Username is correct
- Password is correct
- Host is correct
- Port is correct
- `DATABASE_URL` is correctly configured

---

## Alembic migration fails

Check:

- SQLAlchemy model definitions
- Alembic configuration
- Database connection
- Existing migration history
- Whether the migration has already been applied

---

## Uploaded file cannot be opened

Check:

- The file exists inside `uploads/`
- The stored relative path is correct
- FastAPI static-file mounting is configured
- The generated browser URL points to the correct resource

---

## Streamlit frontend cannot communicate with backend

Check:

- FastAPI is running
- Backend URL used by Streamlit is correct
- API endpoints match the current backend
- Request/response fields match the current Pydantic schemas
- The frontend is using the current backend structure

---

# 📈 Future Improvements

Possible future extensions include:

- User authentication and authorization
- Multiple users
- Todo categories
- Search and filtering
- Sorting by priority
- Pagination
- Better file validation
- File deletion when a Todo is deleted
- Automated tests with Pytest
- Docker containerization
- Production deployment
- Environment-specific configuration
- Structured logging
- API versioning
- Automated CI/CD through GitHub Actions
- More advanced frontend UX

---

# 🎯 Project Goals

The main purpose of this project is not simply to create a Todo list.

It demonstrates the progression from a basic Python program to a more complete backend application:

```text
Python Fundamentals
        ↓
FastAPI
        ↓
REST APIs
        ↓
Pydantic
        ↓
PostgreSQL
        ↓
SQLAlchemy
        ↓
Alembic
        ↓
File Handling
        ↓
Streamlit
        ↓
Git & GitHub
```

The project therefore serves as a practical demonstration of backend development concepts using Python.

---

# 👨‍💻 Author

**Amanat**

BS Artificial Intelligence Student

This project was developed as a practical learning project while working with:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Streamlit
- Git
- GitHub

---

# ⭐ Project Summary

The Todo application evolved from a simple in-memory Todo program into a structured full-stack application.

Its current architecture combines:

```text
┌──────────────────────────────┐
│          Frontend            │
│          Streamlit           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           Backend            │
│           FastAPI            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│             ORM              │
│          SQLAlchemy          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           Database           │
│          PostgreSQL          │
└──────────────────────────────┘

              ▲
              │
       ┌──────┴──────┐
       │   Alembic   │
       │  Migrations │
       └─────────────┘

              +

       ┌─────────────┐
       │   uploads/  │
       │    Files    │
       └─────────────┘
```

It demonstrates the core principles required to build a database-backed Python API with a dedicated frontend, schema migration system, persistent storage, CRUD functionality, file handling, and version-controlled development.

**Built with Python 🐍 · FastAPI ⚡ · PostgreSQL 🐘 · SQLAlchemy 🔗 · Alembic 🛠️ · Streamlit 🎈 · Git/GitHub 🌿**
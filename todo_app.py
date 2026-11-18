import os
from pathlib import Path
from uuid import uuid4

from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    status,
    Depends,
    UploadFile,
    File,
    Form
)

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import TodoModel
from datetime import datetime
from fastapi.staticfiles import StaticFiles


# =========================================================
# CONFIGURATION
# =========================================================

UPLOAD_DIR = Path("uploads")

# Create uploads folder if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)


# Create database tables if they don't exist yet
Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Simple Todo API",
    description="A basic Todo application using FastAPI and PostgreSQL",
    version="2.0.0",
)


# =========================================================
# STATIC FILES
# =========================================================

# Make uploaded files accessible through the browser
app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads"
)


# =========================================================
# PYDANTIC MODELS
# =========================================================

class Todo(BaseModel):

    # Todo ID
    id: int

    # Todo text
    title: str

    # Completion status
    completed: bool

    # Creation time
    created_at: datetime

    # Update time
    updated_at: datetime

    # Optional uploaded file
    file_path: str | None = None

    # Allow SQLAlchemy objects
    model_config = {
        "from_attributes": True
    }


# =========================================================
# DATABASE SESSION
# =========================================================

def get_db():

    # Create database session
    db = SessionLocal()

    try:

        # Give the session to the endpoint
        yield db

    finally:

        # Close the session
        db.close()


# =========================================================
# FILE HELPERS
# =========================================================

async def save_uploaded_file(file: UploadFile) -> str:
    """Save an uploaded file using a unique filename."""

    # Get original file extension
    extension = Path(file.filename or "").suffix

    # Generate unique filename
    unique_filename = f"{uuid4().hex}{extension}"

    # Build physical file path
    physical_path = UPLOAD_DIR / unique_filename

    # Read uploaded file
    contents = await file.read()

    # Save file
    with open(physical_path, "wb") as f:
        f.write(contents)

    # Return database path
    return f"uploads/{unique_filename}"


def delete_physical_file(file_path: str | None):
    """Delete a stored file from the uploads folder."""

    if not file_path:
        return

    # Get only the filename
    filename = Path(file_path).name

    # Build physical path
    physical_path = UPLOAD_DIR / filename

    # Delete if it exists
    if physical_path.exists():
        physical_path.unlink()


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Todo API is running"
    }


# =========================================================
# CREATE TODO + OPTIONAL FILE
# =========================================================

@app.post(
    "/todos",
    response_model=Todo,
    status_code=status.HTTP_201_CREATED
)
async def create_todo(

    # Todo text
    title: str = Form(...),

    # Optional uploaded file
    file: UploadFile | None = File(None),

    # Database session
    db: Session = Depends(get_db)
):

    # Start with no file
    file_path = None

    # Save file if provided
    if file is not None:
        file_path = await save_uploaded_file(file)

    # Create Todo
    todo = TodoModel(
        title=title,
        completed=False,
        file_path=file_path
    )

    # Add to database
    db.add(todo)

    # Save
    db.commit()

    # Refresh
    db.refresh(todo)

    return todo


# =========================================================
# GET ALL TODOS
# =========================================================

@app.get("/todos", response_model=list[Todo])
def get_todos(
    completed: bool | None = Query(
        default=None,
        description="Filter Todos by completion status"
    ),
    db: Session = Depends(get_db)
):

    # Start query
    query = db.query(TodoModel)

    # Apply completion filter
    if completed is not None:
        query = query.filter(
            TodoModel.completed == completed
        )

    # Get Todos
    todo_list = query.all()

    return todo_list


# =========================================================
# GET ONE TODO
# =========================================================

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):

    # Find Todo
    todo = db.query(TodoModel).filter(
        TodoModel.id == todo_id
    ).first()

    # Todo doesn't exist
    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return todo


# =========================================================
# UPDATE TODO + OPTIONAL FILE
# =========================================================

@app.put(
    "/todos/{todo_id}",
    response_model=Todo
)
async def update_todo(

    # Todo ID
    todo_id: int,

    # Optional new title
    title: str | None = Form(None),

    # Optional completion status
    completed: bool | None = Form(None),

    # Optional replacement file
    file: UploadFile | None = File(None),

    # Whether to remove the current file
    remove_file: bool = Form(False),

    # Database session
    db: Session = Depends(get_db)
):

    # Find Todo
    todo = db.query(TodoModel).filter(
        TodoModel.id == todo_id
    ).first()

    # Todo doesn't exist
    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    # Update title
    if title is not None:

        if not title.strip():

            raise HTTPException(
                status_code=400,
                detail="Todo title cannot be empty"
            )

        todo.title = title

    # Update completion status
    if completed is not None:
        todo.completed = completed

    # -----------------------------------------------------
    # FILE HANDLING
    # -----------------------------------------------------

    # If a new file is uploaded
    if file is not None:

        # Remember old file
        old_file_path = todo.file_path

        # Save new file
        new_file_path = await save_uploaded_file(file)

        # Update database path
        todo.file_path = new_file_path

        # Delete old file
        delete_physical_file(old_file_path)

    # Otherwise, remove existing file if requested
    elif remove_file:

        # Delete physical file
        delete_physical_file(todo.file_path)

        # Remove database reference
        todo.file_path = None

    # Save changes
    db.commit()

    # Refresh
    db.refresh(todo)

    return todo


# =========================================================
# DELETE TODO
# =========================================================

@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):

    # Find Todo
    todo = db.query(TodoModel).filter(
        TodoModel.id == todo_id
    ).first()

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    # Delete attached physical file
    delete_physical_file(todo.file_path)

    # Delete database record
    db.delete(todo)

    # Save
    db.commit()

    return {
        "message": "Todo deleted successfully"
    }


# =========================================================
# DELETE ALL TODOS
# =========================================================

@app.delete("/todos")
def delete_all_todos(
    db: Session = Depends(get_db)
):

    # Get all Todos
    todos = db.query(TodoModel).all()

    # Delete physical files
    for todo in todos:
        delete_physical_file(todo.file_path)

    # Delete database records
    for todo in todos:
        db.delete(todo)

    # Save
    db.commit()

    return {
        "message": "All Todos deleted successfully"
    }
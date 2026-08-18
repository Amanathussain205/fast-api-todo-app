import os

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
from database import engine, Base, SessionLocal
from models import TodoModel
from datetime import datetime
from fastapi.staticfiles import StaticFiles


# Create FastAPI application
app = FastAPI(
    title="Simple Todo API",
    description="A basic Todo application using FastAPI and PostgreSQL",
    version="2.0.0",
)


# Make the uploads folder accessible through the browser
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# =========================================================
# PYDANTIC MODELS
# =========================================================

class TodoUpdate(BaseModel):

    # New Todo title
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    # New completion status
    completed: bool | None = None


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
# HOME
# =========================================================

@app.get("/")
def home():

    # Simple health message
    return {"message": "Todo API is running"}


# =========================================================
# CREATE TODO + OPTIONAL FILE
# =========================================================

@app.post(
    "/todos",
    response_model=Todo,
    status_code=status.HTTP_201_CREATED
)
async def create_todo(

    # Todo text from the form
    title: str = Form(...),

    # Optional file
    file: UploadFile | None = File(None),

    # Database session
    db: Session = Depends(get_db)
):

    # Start with no file path
    file_path = None

    # If the user uploaded a file
    if file is not None:

        # Create uploads folder if it doesn't exist
        os.makedirs("uploads", exist_ok=True)

        # Create the file path
        file_path = f"uploads/{file.filename}"

        # Read the uploaded file
        contents = await file.read()

        # Save the actual file
        with open(file_path, "wb") as f:
            f.write(contents)

    # Create ONE Todo database record
    todo = TodoModel(
        title=title,
        completed=False,
        file_path=file_path
    )

    # Add Todo to database session
    db.add(todo)

    # Save to PostgreSQL
    db.commit()

    # Get generated Todo ID
    db.refresh(todo)

    # Return the ONE Todo
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

    # Query all Todos
    query = db.query(TodoModel)

    # Apply completion filter
    if completed is not None:
        query = query.filter(
            TodoModel.completed == completed
        )

    # Get results
    todo_list = query.all()

    # Return Todos
    return todo_list


# =========================================================
# GET ONE TODO
# =========================================================

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):

    # Find Todo by ID
    todo = db.query(TodoModel).filter(
        TodoModel.id == todo_id
    ).first()

    # If not found
    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    # Return Todo
    return todo


# =========================================================
# UPDATE TODO
# =========================================================

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db)
):

    # Find Todo
    todo = db.query(TodoModel).filter(
        TodoModel.id == todo_id
    ).first()

    # If not found
    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    # Update title if provided
    if todo_data.title is not None:
        todo.title = todo_data.title

    # Update completion status if provided
    if todo_data.completed is not None:
        todo.completed = todo_data.completed

    # Save changes
    db.commit()

    # Refresh Todo
    db.refresh(todo)

    # Return Todo
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

    # If not found
    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    # Delete Todo
    db.delete(todo)

    # Save deletion
    db.commit()

    # Return confirmation
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

    # Get all Todo records
    todos = db.query(TodoModel).all()

    # Delete every Todo
    for todo in todos:
        db.delete(todo)

    # Save the deletion
    db.commit()

    # Return confirmation
    return {
        "message": "All Todos deleted successfully"
    }
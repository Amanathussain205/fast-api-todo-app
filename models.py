from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime


# SQLAlchemy model representing the "todos" table
class TodoModel(Base):

    # Name of the table in PostgreSQL
    __tablename__ = "todos"

    # Todo ID
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    # Todo text
    title: Mapped[str] = mapped_column(
        String(100)
    )

    # Completion status
    completed: Mapped[bool] = mapped_column(
        default=False
    )

    # Todo priority
    priority: Mapped[int] = mapped_column(
        default=1
    )

    # When the Todo was created
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now
    )

    # When the Todo was updated
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now
    )

    # Optional uploaded file path
    file_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
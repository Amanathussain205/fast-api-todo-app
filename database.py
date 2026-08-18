from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# PostgreSQL database URL
DATABASE_URL = "postgresql+psycopg://postgres:Amanat@localhost:5433/todo_db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a Session factory
SessionLocal = sessionmaker(bind=engine)


# Base class for our database models
class Base(DeclarativeBase):
    pass
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load settings from the .env file (never commit .env)
load_dotenv()

# PostgreSQL database URL, read from the environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Copy .env.example to .env and fill it in."
    )

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a Session factory
SessionLocal = sessionmaker(bind=engine)


# Base class for our database models
class Base(DeclarativeBase):
    pass

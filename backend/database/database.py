from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine to connect to the database
engine = create_engine(DATABASE_URL, echo=True)

# Create a SessionLocal class for managing sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the ORM models
Base = declarative_base()

# Dependency function to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
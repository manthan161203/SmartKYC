from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database

from backend.config.config import Config
from backend.database.models import Base

if not hasattr(Config, "DATABASE_URL") or not Config.DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the configuration.")

DATABASE_URL = Config.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database_if_not_exists():
    try:
        db_name = engine.url.database
        print(f"Checking if database '{db_name}' exists...")
        
        if not database_exists(engine.url):
            print(f"Database '{db_name}' does not exist. Creating...")
            create_database(engine.url)
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")
    
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: Database creation error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error while creating the database: {e}")
        raise

def create_tables():
    try:
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: Table creation error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error while creating tables: {e}")
        raise

def get_db():
    db = SessionLocal()
    try:
        print("Starting a new database session...")
        yield db
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: Database session error: {e}")
        db.rollback()
        raise
    except Exception as e:
        print(f"Unexpected error during database session: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        print("Database session closed.")
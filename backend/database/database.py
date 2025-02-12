from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database
from backend.config.config import Config
from backend.database.models import Base

DATABASE_URL = Config.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database_if_not_exists():
    try:
        print(f"Checking if database '{engine.url.database}' exists...")
        if not database_exists(engine.url):
            print(f"Database '{engine.url.database}' does not exist. Creating database...")
            create_database(engine.url)
            print(f"Database '{engine.url.database}' created successfully!")
        else:
            print(f"Database '{engine.url.database}' already exists.")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: An error occurred while checking or creating the database: {e}")
        raise
    except Exception as e:
        print(f"Exception: An unexpected error occurred while checking or creating the database: {e}")
        raise 

def create_tables():
    try:
        print("Creating tables if they do not exist...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError: An error occurred while creating the tables: {e}")
        raise
    except Exception as e:
        print(f"Exception: An unexpected error occurred while creating the tables: {e}")
        raise

def get_db():
    try:
        print("Starting a new database session...")
        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"Error while starting a database session: {e}")
    finally:
        db.close()
        print("Database session closed.")
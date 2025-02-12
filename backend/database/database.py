import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database
from backend.config.config import Config
from backend.database.models import Base

DATABASE_URL = Config.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig(
    filename='database_setup.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def create_database_if_not_exists():
    try:
        logging.info(f"Checking if database '{engine.url.database}' exists...")
        if not database_exists(engine.url):
            logging.info(f"Database '{engine.url.database}' does not exist. Creating database...")
            create_database(engine.url)
            logging.info(f"Database '{engine.url.database}' created successfully!")
        else:
            logging.info(f"Database '{engine.url.database}' already exists.")
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: An error occurred while checking or creating the database: {e}", exc_info=True)  # Log error with stack trace
        raise
    except Exception as e:
        logging.error(f"Exception: An unexpected error occurred while checking or creating the database: {e}", exc_info=True)  # Log error with stack trace
        raise 

def create_tables():
    try:
        logging.info("Creating tables if they do not exist...")
        Base.metadata.create_all(bind=engine)
        logging.info("Tables created successfully!")
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: An error occurred while creating the tables: {e}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"Exception: An unexpected error occurred while creating the tables: {e}", exc_info=True)
        raise

def get_db():
    try:
        logging.info("Starting a new database session...")
        db = SessionLocal()
        yield db
    except Exception as e:
        logging.error(f"Error while starting a database session: {e}", exc_info=True)
    finally:
        db.close()
        logging.info("Database session closed.")

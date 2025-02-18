import logging
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database

from backend.config.config import Config
from backend.database.models.base_model import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = None
SessionLocal = None

def init_db():
    global engine, SessionLocal

    if not hasattr(Config, "DATABASE_URL") or not Config.DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the configuration.")

    DATABASE_URL = Config.DATABASE_URL

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        db_name = engine.url.database
        logger.info(f"Checking if database '{db_name}' exists...")

        if not database_exists(engine.url):
            logger.info(f"Database '{db_name}' does not exist. Creating...")
            create_database(engine.url)
            logger.info(f"Database '{db_name}' created successfully!")

        # Check if tables already exist
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        if not existing_tables:
            logger.info("No tables found. Creating tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("Tables created successfully!")
        else:
            logger.info("Tables already exist. Skipping table creation.")

    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError: Error occurred during DB initialization: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during DB initialization: {e}")
        raise
    
def get_db():
    db = SessionLocal()
    try:
        logger.info("Starting a new database session...")
        yield db
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError: Database session error: {e}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database session: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.info("Database session closed.")

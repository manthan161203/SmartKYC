import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.config.config import settings
from backend.models.base_model import Base
from backend.models import (
    user_model, base_model, document_model, document_type_model,  # noqa: F401
    gender_type_model, kyc_status_model, otp_model, otp_status_model, user_address_model  # noqa: F401
)
from typing import Generator

# --------------------- Logging Configuration ---------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("smart_kyc.log"),  # Save logs to file
        logging.StreamHandler()  # Print logs to console
    ]
)
logger = logging.getLogger(__name__)

# --------------------- Database Connection ---------------------
try:
    # Create the database engine
    engine = create_engine(settings.DATABASE_URL, future=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("✅ Database engine created successfully.")
except Exception as e:
    logger.critical(f"❌ Failed to create database engine: {e}")
    raise e

# --------------------- Database Initialization ---------------------
def init_db() -> bool:
    """
    Initializes the database and creates tables if they do not exist.

    Returns:
        bool: True if initialization is successful, raises an exception otherwise.
    """
    try:
        logger.info("🚀 Initializing Database...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database Initialized Successfully!")
        return True  # Return success
    except Exception as e:
        logger.critical(f"❌ Database Initialization Failed: {e}")
        raise e

# --------------------- Database Session Dependency ---------------------
def get_db() -> Generator[Session, None, None]:
    """
    Provides a new database session for each request.
    Ensures proper session handling with automatic closing.

    Yields:
        Session: SQLAlchemy session instance.
    """
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"⚠️ Database session error: {e}")
        raise e  # Ensure proper exception handling
    finally:
        db.close()
        logger.info("🔄 Database session closed.")
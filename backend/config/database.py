import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config.config import settings
from backend.models.base_model import Base
from backend.models import user_model, base_model, document_model, document_type_model, gender_type_model ,kyc_status_model ,otp_model, otp_status_model, user_address_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the database engine
engine = create_engine(settings.DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initializes the database and creates tables if they do not exist.
    """
    logger.info("Initializing Database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database Initialized Successfully!")

def get_db():
    """
    Dependency to provide a database session.
    Ensures proper session handling with automatic closing.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

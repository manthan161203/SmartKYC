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
        logging.FileHandler("smart_kyc.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --------------------- Database Connection ---------------------
try:
    engine = create_engine(settings.DATABASE_URL, future=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("✅ Database engine created successfully.")
except Exception as e:
    logger.critical(f"❌ Failed to create database engine: {e}")
    raise e

# --------------------- Database Initialization ---------------------
def init_db() -> bool:
    try:
        logger.info("🚀 Initializing Database...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database Initialized Successfully!")
        return True
    except Exception as e:
        logger.critical(f"❌ Database Initialization Failed: {e}")
        raise e

# --------------------- Database Session Dependency ---------------------
def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"⚠️ Database session error: {e}")
        raise e
    finally:
        db.close()
        logger.info("🔄 Database session closed.")
import logging
import secrets
from pydantic_settings import BaseSettings

# --------------------- Logging Configuration ---------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("smart_kyc.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs to console
    ]
)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Configuration settings for the Smart KYC application.
    Loads values from environment variables and `.env` file.
    """

    # Database Configuration
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str = "kyc_db"
    DB_PASSWORD: str
    ALEMBIC_DB_PASSWORD: str

    # Email Configuration
    SENDER_MAIL: str
    PASSKEY_MAIL: str
    SMTP_PORT: int
    SMTP_SERVER: str

    # JWT Configuration
    JWT_SECRET_KEY: str = secrets.token_urlsafe(64)  # Generates a secure random key
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 day
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # OTP Configuration
    OTP_EXPIRY_TIME: int = 600  # 10 minutes

    # CORS Configuration
    allow_origins: list[str] = ["*"]  # Configurable CORS origins
    
    # OPENAI Configuration
    OPENAI_KEY: str
    
    class Config:
        """
        Configuration for Pydantic BaseSettings.
        Loads values from a `.env` file if present.
        """
        env_file = ".env"  # Automatically loads environment variables from .env
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        """
        Constructs and returns the main database URL.
        """
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def ALEMBIC_DATABASE_URL(self) -> str:
        """
        Constructs and returns the Alembic database URL.
        """
        return f"mysql+pymysql://{self.DB_USER}:{self.ALEMBIC_DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# --------------------- Load Settings ---------------------
try:
    settings = Settings()
    logger.info("✅ Environment variables loaded successfully.")
except Exception as e:
    logger.critical(f"❌ Error loading environment variables: {e}", exc_info=True)
    raise e

import logging
import secrets
from pydantic_settings import BaseSettings

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

class Settings(BaseSettings):

    # Database Configuration
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str = "kyc_db"
    DB_PASSWORD: str
    ALEMBIC_DB_PASSWORD: str
    DB_SCHEMA: str
    # Email Configuration
    SENDER_MAIL: str
    PASSKEY_MAIL: str
    SMTP_PORT: int
    SMTP_SERVER: str

    # JWT Configuration
    JWT_SECRET_KEY: str = secrets.token_urlsafe(64)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080
    
    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # OTP Configuration
    OTP_EXPIRY_TIME: int = 600  # 10 minutes

    # CORS Configuration
    allow_origins: list[str] = ["*"]
    
    # OPENAI Configuration
    OPENAI_KEY: str
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    @property
    def ALEMBIC_DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.ALEMBIC_DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # return f"postgresql://{self.DB_USER}:{self.ALEMBIC_DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def CLOUDINARY_URL(self) -> str:
        return f"cloudinary://{self.CLOUDINARY_API_KEY}:{self.CLOUDINARY_API_SECRET}@{self.CLOUDINARY_CLOUD_NAME}"

# --------------------- Load Settings ---------------------
try:
    settings = Settings()
    logger.info("✅ Environment variables loaded successfully.")
except Exception as e:
    logger.critical(f"❌ Error loading environment variables: {e}", exc_info=True)
    raise e

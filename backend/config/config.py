from pydantic_settings import BaseSettings

class Settings(BaseSettings):
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

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    BACKEND_URL : str
    
    class Config:
        env_file = ".env"  # Automatically loads .env file

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

# Initialize settings
settings = Settings()

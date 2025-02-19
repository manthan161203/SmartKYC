import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME", "kyc_db")
    
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PASSWORD_ALEMBIC = os.getenv("DB_PASSWORD_ALEMBIC")

    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    DATABASE_URL_ALEMBIC = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD_ALEMBIC}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SENDER_MAIL = os.getenv("SENDER_MAIL")
    PASSKEY_MAIL = os.getenv("PASSKEY_MAIL")
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"

    
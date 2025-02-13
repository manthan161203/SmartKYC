import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PASSWORD_ALEMBIC = os.getenv("DB_PASSWORD_ALEMBIC")
    DB_NAME = os.getenv("DB_NAME", "kyc_db")
    
    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    DATABASE_URL_ALEMBIC = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD_ALEMBIC}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
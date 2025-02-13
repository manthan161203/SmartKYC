import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PASSWORD_ALEMBIC = os.getenv("DB_PASSWORD_ALEMBIC")
    DB_NAME = os.getenv("DB_NAME", "kyc_db")  # Default database name (kyc_db if not provided)

    # Construct the DATABASE_URL for connecting to the database
    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Construct a separate DATABASE_URL for Alembic migrations (in case different credentials are used)
    DATABASE_URL_ALEMBIC = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD_ALEMBIC}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

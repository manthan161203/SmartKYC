import sys
import os
import logging
from logging.config import fileConfig
from sqlalchemy import create_engine, text, pool
from sqlalchemy.exc import OperationalError
from alembic import context

from backend.config.config import settings
from backend.models.base_model import Base
from backend.models import base_model, document_model, document_type_model, gender_type_model, kyc_status_model, otp_model, otp_status_model, user_model, user_address_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = context.config
config.set_main_option("sqlalchemy.url", settings.ALEMBIC_DATABASE_URL)

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def create_database_if_not_exists():
    """
    Ensures the database exists before running migrations.
    """
    db_url_parts = settings.DATABASE_URL.rsplit("/", 1)
    db_root_url = db_url_parts[0] + "/"
    db_name = db_url_parts[1]

    root_engine = create_engine(db_root_url, isolation_level="AUTOCOMMIT")

    with root_engine.connect() as conn:
        existing_databases = conn.execute(text("SHOW DATABASES;")).fetchall()
        existing_db_names = [db[0] for db in existing_databases]

        if db_name not in existing_db_names:
            logger.info(f"Database '{db_name}' not found. Creating it now...")
            conn.execute(text(f"CREATE DATABASE {db_name};"))
            logger.info(f"Database '{db_name}' created successfully!")
        else:
            logger.info(f"Database '{db_name}' already exists.")

def run_migrations_offline():
    """
    Runs migrations in 'offline' mode without an active database connection.
    """
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    Runs migrations in 'online' mode with an active database connection.
    """
    create_database_if_not_exists()
    
    connectable = create_engine(settings.DATABASE_URL, poolclass=pool.NullPool)
    
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    logger.info("Running migrations in offline mode...")
    run_migrations_offline()
else:
    logger.info("Running migrations in online mode...")
    run_migrations_online()

# import logging
# from sqlalchemy import create_engine, NullPool, inspect, text
# from sqlalchemy.orm import sessionmaker, Session
# from backend.config.config import settings
# from backend.models.base_model import Base
# from backend.models import (
#     user_model, base_model, document_model, document_type_model,  document_details_model, # noqa: F401
#     gender_type_model, kyc_status_model, otp_model, otp_status_model, user_address_model  # noqa: F401
# )
# from typing import Generator

# # --------------------- Logging Configuration ---------------------
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler("smart_kyc.log"),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# # --------------------- Database Connection ---------------------
# try:
#     engine = create_engine(settings.DATABASE_URL, future=True, poolclass=NullPool)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     logger.info("✅ Database engine created successfully.")
# except Exception as e:
#     logger.critical(f"❌ Failed to create database engine: {e}")
#     raise e

# # --------------------- Apply RLS for All Tables ---------------------
# def setup_rls():
#     try:
#         logger.info("🔒 Enabling Row-Level Security (RLS) for all tables...")

#         inspector = inspect(engine)
#         tables = inspector.get_table_names()

#         with engine.connect() as connection:
#             for table in tables:
#                 # Enable RLS for each table
#                 connection.execute(text(f"ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;"))

#                 # Fetch existing policies for the table
#                 existing_policies_query = text(f"""
#                     SELECT policyname FROM pg_policies WHERE schemaname = 'public' AND tablename = '{table}';
#                 """)
#                 existing_policies = {row[0] for row in connection.execute(existing_policies_query).fetchall()}

#                 # Define policies
#                 policies = {
#                     f"Allow authenticated users to read {table}": f"""
#                         CREATE POLICY "Allow authenticated users to read {table}"
#                         ON public.{table}
#                         FOR SELECT
#                         USING (auth.role() = 'authenticated');
#                     """,
#                     f"Allow authenticated users to insert {table}": f"""
#                         CREATE POLICY "Allow authenticated users to insert {table}"
#                         ON public.{table}
#                         FOR INSERT
#                         WITH CHECK (auth.role() = 'authenticated');
#                     """,
#                     f"Allow authenticated users to update {table}": f"""
#                         CREATE POLICY "Allow authenticated users to update {table}"
#                         ON public.{table}
#                         FOR UPDATE
#                         USING (auth.role() = 'authenticated');
#                     """,
#                     f"Allow authenticated users to delete {table}": f"""
#                         CREATE POLICY "Allow authenticated users to delete {table}"
#                         ON public.{table}
#                         FOR DELETE
#                         USING (auth.role() = 'authenticated');
#                     """
#                 }

#                 # Create only missing policies
#                 for policy_name, policy_sql in policies.items():
#                     if policy_name not in existing_policies:
#                         connection.execute(text(policy_sql))
#                         logger.info(f"✅ Created RLS policy: {policy_name} on {table}")
#                     else:
#                         logger.info(f"🔄 Skipped existing RLS policy: {policy_name} on {table}")

#             connection.commit()
#         logger.info("✅ RLS enabled and policies applied for all tables!")
#     except Exception as e:
#         logger.critical(f"❌ Failed to set up RLS: {e}")
#         raise e
    
# # --------------------- Database Initialization ---------------------
# def init_db() -> bool:
#     try:
#         logger.info("🚀 Initializing Database...")
#         Base.metadata.create_all(bind=engine)
#         # setup_rls()
#         logger.info("✅ Database Initialized Successfully!")
#         return True
#     except Exception as e:
#         logger.critical(f"❌ Database Initialization Failed: {e}")
#         raise e

# # --------------------- Database Session Dependency ---------------------
# def get_db() -> Generator[Session, None, None]:
#     db: Session = SessionLocal()
#     try:
#         yield db
#     except Exception as e:
#         logger.error(f"⚠️ Database session error: {e}")
#         raise e
#     finally:
#         db.close()
#         logger.info("🔄 Database session closed.")




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
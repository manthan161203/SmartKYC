import logging
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from backend.config.database import init_db, get_db
from backend.utils.jwt_middleware import get_current_user
from backend.utils.seed_data import seed_reference_tables
from backend.routes.auth_route import router as auth_router
from backend.routes.user_route import router as user_router
from backend.routes.document_route import router as document_router
from fastapi.middleware.cors import CORSMiddleware
from backend.config.config import settings
from typing import AsyncGenerator, Dict

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

# --------------------- Lifespan Event ---------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler for FastAPI.
    Handles setup and teardown operations, including database initialization.
    """
    try:
        logger.info("🚀 Starting Smart KYC application...")
        
        # Initialize the database
        if not init_db():
            logger.critical("❌ Database initialization failed. Exiting application.")
            exit(1)

        # Seed reference tables (if applicable)
        seed_reference_tables()
        logger.info("✅ Database initialized and reference tables seeded.")

    except Exception as e:
        logger.critical(f"❌ Critical error during startup: {e}")
        exit(1)

    yield  # Hand over control to the application

    logger.info("🛑 Shutting down Smart KYC application...")

# --------------------- FastAPI Application ---------------------
app = FastAPI(lifespan=lifespan)

# --------------------- CORS Middleware ---------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,  # Use settings for flexibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("🌍 CORS middleware configured.")

# --------------------- API Routes ---------------------
app.include_router(auth_router)
logger.info("🔐 Authentication routes registered.")

app.include_router(user_router, dependencies=[Depends(get_current_user)])
logger.info("👤 User routes registered (authentication required).")

app.include_router(document_router)
logging.info("Documents routes registered")

# --------------------- API Endpoints ---------------------
@app.get("/", tags=["Root"])
async def read_root() -> Dict[str, str]:
    """
    Root endpoint to check if the Smart KYC API is running.

    Returns:
        Dict[str, str]: A simple status message.
    """
    logger.info("📢 Root endpoint accessed.")
    return {"message": "🚀 Smart KYC API is running!"}

@app.get("/health", tags=["Health"])
async def health_check(db: Session = Depends(get_db)) -> Dict[str, str]:
    """
    Health check endpoint to verify database connectivity.

    Args:
        db (Session): Database session dependency.

    Returns:
        Dict[str, str]: Status of database connectivity.
    """
    try:
        db.execute(text("SELECT 1"))  # Simple DB test query
        logger.info("✅ Health check successful: Database is connected.")
        return {"status": "ok", "message": "Database is connected"}
    except Exception as e:
        logger.error(f"⚠️ Health check failed: {e}")
        return {"status": "error", "message": str(e)}

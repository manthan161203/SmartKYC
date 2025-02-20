import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.config.database import init_db
from backend.utils.seed_data import seed_reference_tables
from backend.routes.auth_route import router as auth_router
from backend.routes.user_route import router as user_router
from backend.routes.otp_route import router as otp_router

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application lifespan events.
    Initializes the database and seeds fixed reference data on startup,
    and performs cleanup on shutdown.
    """
    try:
        logger.info("🚀 Starting Smart KYC application...")
        init_db()
        seed_reference_tables()
        logger.info("✅ Database initialized and reference tables seeded.")
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
        raise e

    yield  # Application runs here

    logger.info("🛑 Shutting down Smart KYC application...")

# Initialize FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

# Include authentication, user, and OTP routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(otp_router, prefix="/otp", tags=["OTP Verification"])

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "🚀 Smart KYC API is running!"}

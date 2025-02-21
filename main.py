import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.config.database import init_db
from backend.utils.seed_data import seed_reference_tables
from backend.routes.auth_route import router as auth_router
from backend.routes.profile_route import router as profile_router  # Updated

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for application lifespan events"""
    try:
        logger.info("🚀 Starting Smart KYC application...")
        init_db()
        seed_reference_tables()
        logger.info("✅ Database initialized and reference tables seeded.")
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
        raise e

    yield

    logger.info("🛑 Shutting down Smart KYC application...")

# Initialize FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(auth_router)
app.include_router(profile_router)

@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint to check if the API is running"""
    return {"message": "🚀 Smart KYC API is running!"}

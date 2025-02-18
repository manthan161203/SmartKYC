import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.config.database import init_db
from backend.routes import register_route
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Initializing the database.")
        init_db()
        logger.info("Database initialized successfully.")
        yield
    except SQLAlchemyError as e:
        logger.error(f"Database initialization failed: {e}")
        raise RuntimeError("Failed to initialize the database. Check logs for details.")
    except Exception as e:
        logger.error(f"Unexpected error during startup: {e}")
        raise RuntimeError("Unexpected startup error. Check logs.")
    finally:
        logger.info("Shutting down the application.")

app = FastAPI(lifespan=lifespan)

app.include_router(register_route.router)

@app.get("/")
def read_root():
    logger.info("Root endpoint was accessed.")
    return {"message": "Welcome to the KYC system!"}

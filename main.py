import logging
from fastapi import FastAPI
from backend.database.database import get_db
from backend.routes import register

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("FastAPI app has started.")

get_db()

app.include_router(register.router)

@app.get("/")
def read_root():
    logger.info("Root endpoint was accessed.")
    return {"message": "Welcome to the KYC system!"}

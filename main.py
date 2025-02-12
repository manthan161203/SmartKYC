import logging
from backend.database.database import create_database_if_not_exists, create_tables

def main():
    logging.info("Starting database setup...")  # Log the start of the operation
    try:
        create_database_if_not_exists()
        create_tables()
        logging.info("Database setup completed successfully!")  # Log success
    except Exception as e:
        logging.error(f"Error in database setup: {e}", exc_info=True)  # Log error with stack trace

if __name__ == "__main__":
    logging.basicConfig(
        filename='database_setup.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    main()

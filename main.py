from backend.database.database import create_database_if_not_exists, create_tables

def main():
    print("Starting database setup...")
    try:
        create_database_if_not_exists()
        create_tables()
        print("Database setup completed successfully!")
    except Exception as e:
        print(f"Error in database setup: {e}")

if __name__ == "__main__":
    main()
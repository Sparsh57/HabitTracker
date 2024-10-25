# main.py

from src.database_management import DatabaseHandler, create_tables


def main():
    db_handler = DatabaseHandler(db_path='data/maindatabase.db')
    db_handler.connect_database()

    # Create tables
    create_tables(db_handler)

    # Close the database connection
    db_handler.close_connection()


if __name__ == '__main__':
    main()

import sqlite3
from sqlite3 import Error
import os


class DatabaseHandler:
    def __init__(self, db_path):
        """
        Initialize the database handler with the path to the database file.

        :param db_path: The file path to the SQLite database.
        """
        self.db_path = db_path
        self.conn = None

    def connect_database(self):
        """Create a database connection to the SQLite database specified by db_path."""
        try:
            # Ensure the directory for the database exists
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)

            self.conn = sqlite3.connect(self.db_path)
            print(f"Connected to database at: {self.db_path}")
        except Error as e:
            print(f"Error connecting to database at {self.db_path}: {e}")
            raise

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
            self.conn = None

    def execute_query(self, query, params=()):
        """Execute a write operation (INSERT, UPDATE, DELETE)."""
        if not self.conn:
            self.connect_database()
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            print(f"Query executed successfully: {query}")
            return True
        except Error as e:
            print(f"Database operation error: {e}")
            if self.conn:
                self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query, params=()):
        """Execute a read operation (SELECT) and fetch all results."""
        if not self.conn:
            self.connect_database()
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            print(f"Data fetched successfully: {query}")
            return result
        except Error as e:
            print(f"Database operation error: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def update_status(self, ftp_location, row_id):
        """Update the status of an entry in the database."""
        update_query = """
            UPDATE Maindb
            SET filePath = ?, status = 'Y'
            WHERE rowid = ?
        """
        return self.execute_query(update_query, (ftp_location, row_id))

    def delete_entry(self, file_path):
        """Delete an entry from the database based on the file path."""
        delete_query = "DELETE FROM Maindb WHERE filePath = ?"
        return self.execute_query(delete_query, (file_path,))

    def insert_data(self, table_name, data_dict):
        """Insert data into the specified table."""
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['?'] * len(data_dict))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.execute_query(insert_query, tuple(data_dict.values()))


def create_tables(db_handler):
    create_habits_table = """
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        start_date DATE DEFAULT CURRENT_DATE,
        frequency TEXT,
        goal INTEGER,
        is_active BOOLEAN DEFAULT 1
    );
    """
    create_habit_records_table = """
    CREATE TABLE IF NOT EXISTS habit_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        date DATE DEFAULT CURRENT_DATE,
        notes TEXT,
        FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
    );
    """
    db_handler.execute_query(create_habits_table)
    db_handler.execute_query(create_habit_records_table)

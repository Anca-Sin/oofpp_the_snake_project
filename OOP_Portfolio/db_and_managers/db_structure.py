from .database import Database
from ..helpers.helper_functions import db_connection, close_db_connection
from ..cli.main import HabitTracker
db = Database()
habit_tracker = HabitTracker()

def db_tables() -> None:
    """
    Ensures the required tables exist in the SQLite db.
    Other functions interact with them to store or retrieve data.
    """
    connection = db_connection(habit_tracker, habit_tracker.db.db_filepath)  # Connect to the db
    cursor = connection.cursor()  # Create a cursor object to execute SQL commands

    # Create the "users" table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (     
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing id (int) for each user
            username TEXT NOT NULL UNIQUE          -- Username (str) cannot be left empty (NOT NULL) 
        )                                          --   and must be unique
    """)

    # Create the "habits" table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, 
            habit_name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            creation_date TEXT NOT NULL,
            completions_count INTEGER, -- Count of completions
            checked_off_dates TEXT, -- Comma separated check off dates
            FOREIGN KEY (user_id) REFERENCES users(id) -- Links habits to a specific user in the user table
        )
    """)

    # Create the "streaks" table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streaks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER, 
        current_streak INTEGER,
        current_streak_start TEXT,
        longest_streak INTEGER,
        longest_streak_start TEXT,
        longest_streak_end TEXT,
        streak_length_history TEXT,
        FOREIGN KEY (habit_id) REFERENCES habits(id) -- Link streak to a habit from the habit table
        )
    """)

    connection.commit()  # Commit the changes to the db to make sure the tables are created
    close_db_connection(connection)  # Close the db connection
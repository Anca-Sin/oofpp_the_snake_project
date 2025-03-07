from config import DB_FILEPATH

from helpers.helper_functions import db_connection

def db_tables() -> None:
    """
    Creates the required db tables if they don't already exist.
    The tables use SQLite's foreign key constraints with CASCADE on deletion.

    Schema for the HabitTracker db:
    - users table:   stores user information
    - habits table:  stores habit information with foreign keys to users
    - streaks table: stores streak information with foreign key to habits
    """
    # Connect to the db
    connection = db_connection(DB_FILEPATH)
    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()

    # Create the "users" table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (     
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing ID for each user
            username TEXT NOT NULL UNIQUE          -- Username must be unique and not null
        )                                         
    """)

    # Create the "habits" table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing ID for each habit
            user_id INTEGER,                       -- Foreign key to link habit to a user
            habit_name TEXT NOT NULL,              -- Name of the habit (required)
            frequency TEXT NOT NULL,               -- Frequency (daily/weekly)
            creation_date TEXT NOT NULL,           -- When the habit was created (YYYY-MM-DD)
            completions_count INTEGER,             -- Count of completions
            checked_off_dates TEXT,                -- Comma separated list of completion dates
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- Delete habits when user is deleted
        )
    """)

    # Create the "streaks" table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streaks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Auto-incrementing ID for each streak record
        habit_id INTEGER,                          -- Foreign key to link streak to a habit
        current_streak INTEGER,                    -- Current active streak
        longest_streak INTEGER,                    -- Longest streak achieved
        streak_length_history TEXT,                -- Comma separated list of past streak lengths
        FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE  -- Deletes streaks when habit is deleted
        )
    """)

    # Save the changes to the db
    connection.commit()
    # Close the connection
    connection.close()
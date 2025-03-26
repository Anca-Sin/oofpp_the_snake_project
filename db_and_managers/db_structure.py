"""
Database structure module for the habit tracker app.

Defines and creates the SQLite database schema used by the app.
Propagating the core model separation between classes,it handles tables creation with appropriate relationships
between users, habits, and streaks tables, using foreign key constraints for data integrity.
"""

from config import DB_FILEPATH
from helpers.helper_functions import db_connection

def db_tables() -> None:
    """
    The database's tables.

    Creates three tables with appropriate relationships, which store:
    - users: basic user info
    - habits: habit definitions linked to their user
    - streaks: streak info linked to each habit
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (     
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing ID for each user
            username TEXT NOT NULL UNIQUE          -- Username must be unique and not null
        )                                         
    """)

    # Habits table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing ID for each habit
            user_id INTEGER,                       -- Foreign key to link habit to a user
            habit_name TEXT NOT NULL,              -- Name of the habit (required)
            frequency TEXT NOT NULL,               -- Frequency (daily/weekly)
            creation_date TEXT NOT NULL,           -- When the habit was created (YYYY-MM-DD)
            completions_count INTEGER,             -- Count of completions
            completion_dates TEXT,                 -- Comma separated list of completion dates
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Streak table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streaks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Auto-incrementing ID for each streak record
        habit_id INTEGER,                          -- Foreign key to link streak to a habit
        current_streak INTEGER,                    -- Current active streak
        longest_streak INTEGER,                    -- Longest streak achieved
        streak_length_history TEXT,                -- Comma separated list of past streak lengths
        FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    """)

    connection.commit()
    connection.close()
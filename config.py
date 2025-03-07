"""
Configuration module for the habit tracker application.
This module defines global config variables and functions to modify them.
"""

# Defaults database filepath
DB_FILEPATH = "habit_tracker.db"

def set_db_filepath(filepath: str):
    """
    Sets the global db filepath.

    - allows changing the db filepath at runtime, which is useful for testing or when specified by the user

    Parameters:
        filepath: The new db filepath to use.
    """
    global DB_FILEPATH
    DB_FILEPATH = filepath
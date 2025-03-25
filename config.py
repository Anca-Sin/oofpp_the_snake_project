"""
Configuration settings for the habit tracker app.

This module defines global configuration variable and provides functions to modify them at runtime.
It centralizes configuration value.
"""

# Defaults database filepath
DB_FILEPATH = "habit_tracker.db"

def set_db_filepath(filepath: str):
    """
    Sets the global db filepath.
    Allows changing the db filepath at runtime.

    Parameters:
        filepath: The new db filepath to use.
    """
    global DB_FILEPATH
    DB_FILEPATH = filepath
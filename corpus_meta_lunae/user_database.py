import json
from typing import List, Dict
from user import User
from habit import Habit

class UserDatabase:
    """
    Handles saving and loading user data to/from a JSON file.

    Attributes:
        filepath: The path to the JSON file where user data is stored.
    """

    def __init__(self, filepath: str = "users.json") -> None:
        """
        Initializes the UserDatabase with a file path.

        :param filepath: Path to the JSON file for storing user data.
        """
        self.filepath: Path = Path(filepath) # Convert the string 'filepath' into a Path object for easier file handling
        # Create the file if it doesn't exist to avoid FileNotFound error later
        if not self.filepath.exists():
            self.filepath.write_text("[]") # Start with an empty list in JSON
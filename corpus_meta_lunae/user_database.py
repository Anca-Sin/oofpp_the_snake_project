import json
from typing import List
from .user import User
from .habit import Habit
from pathlib import Path

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

    def _check_if_file_exists(self) -> None:
        """Create the file if it doesn't exist to avoid FileNotFound error later."""
        if not self.filepath.exists():
            self.filepath.write_text("[]") # Start with an empty list in JSON

    def load_users(self) -> List[User]:
        """
        Loads a list of User objects from the JSON file.

        :return: A list of User instances read from the JSON file.
        """
        self._check_if_file_exists()

        raw_json = self.filepath.read_text() # Read the raw JSON string from the file
        data_list = json.loads(raw_json) # Convert the JSON string into a Python list of dict (one for each user)

        users: List[User] = [] # Initialize an empty list to store User objects
        for user_data in data_list:
            user = User() # Create a new User object

            # Get username from the data, default to an empty string to avoid errors
            user.username = user_data.get("username", "")
            # Get the habit list from the data, default to an empty list to avoid errors
            habits_data = user_data.get("habits", [])

            for habit_dict in habits_data:
                habit = Habit() # Create a new Habit object
                habit.name = habit_dict.get("name", "")
                habit.frequency = habit_dict.get("frequency", "")
                user.habits.append(habit) # Add the newly created habit to the user's list of habits

            users.append(user) # Add the fully created User object to the users list

        return users # Return the list of User objects

    def save_users(self, users: List[User]) -> None:
        """
        Saves a list of User objects to the JSON file.

        :param users: A list of User objects to save.
        """
        # Create an empty list to hold dictionaries tha represent each user
        data_list = []
        for user in users:
            user_data = {
                "username": user.username,
                "habits": []
            }

            # Convert each Habit object to a dictionary and add to it user_data
            for habit in user.habits:
                habit_data = {
                    "name": habit.name,
                    "frequency": habit.frequency
                }
                user_data["habits"].append(habit_data)

            data_list.append(user_data)

        # Write the list of dictionaries to the JSON file
        with self.filepath.open("w") as f:
            json.dump(data_list, f, indent=4)
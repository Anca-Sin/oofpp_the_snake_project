from typing import List
from helpers.helper_functions import confirm_input
from db_and_managers.database import Database

class User:
    """
    Represents a user in the habit tracking system.

    Attributes:
        username (str): The username the user registers to use.
        habits (List[Habit]): A list of habits associated with the user.
    """

    def __init__(self, username: str = "", user_id: int = None, db: Database = None) -> None:
        """
        Initializes a User object with a username and an empty list of habits.

        :param username: The username which defaults to an empty string if not provided.
        :param db: An instance of Database to interact with the db
        """
        from .habit import Habit
        self.username: str = username
        self.user_id = user_id
        self.habits: List[Habit] = [] # List to store the user's habits
        self.db = db

    def create_username(self) -> None:
        """Prompts the user to type in a desired username."""
        while True:
            print("Please type in your desired username:")
            username = input().title()
            # Confirm the choice
            confirmed_username = confirm_input("username", username)

            if confirmed_username is not None: # If user confirmed with "yes"
                self.username = confirmed_username
                return
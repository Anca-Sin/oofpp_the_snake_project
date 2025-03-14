import time
from typing import List, Optional

from .habit import Habit
from helpers.colors import GRAY, RES
from helpers.helper_functions import confirm_input


class User:
    """
    The User class serves as central entity.

    - handles username creation
    - has no direct db dependency:
            user_id = assigned in db operations

    Attributes:
        username (str): The username of the user.
        user_id (int): The id from the db of the user.
        habits (List[Habit]): A list of habits associated with the user.
    """

    def __init__(self,
                 username: Optional[str] = None,
                 user_id: Optional[int] = None) -> None:
        """Initializes a new User object with default values."""
        self.username = username
        self.user_id = user_id
        self.habits: List[Habit] = [] # Starts with an empty list of habits

    def create_username(self) -> None:
        """
        Creates a new username.

        - handles input and confirmation
        - checks if the username already exists in the db
        """
        # Avoid circular imports
        from db_and_managers.manager_user_db import username_exists, select_user

        while True:
            # Ask user for username
            print(f"Please type in your desired username {GRAY}or ENTER << to exit{RES} ")
            username = input().title().strip()

            # Exit the loop if "ENTER"
            if not username:
                self.username = None
                return

            # Check if the username already exists
            elif username_exists(username):
                print(f"\nUsername '{username}' is taken! Please try again!")
                time.sleep(1)

            else:
                # Confirm the choice
                confirmed_username = confirm_input("username", username)

                if confirmed_username is not None:
                    self.username = confirmed_username
                    return
                else:
                    # If confirmed input is None on << ENTER
                    return
import time
from typing import List, Optional

from .habit import Habit
from helpers.colors import GRAY, RES
from helpers.helper_functions import confirm_input


class User:
    """
    A registered user, which serves as central entity for the application.

    - handles username creation
    - has no direct db dependency: user_id = assigned externally (in db operations)

    Attributes:
        username: A string assigned by the user.
        user_id:  An integer of the database ID belonging to the username.
        habits:   A list of Habit objects belonging to the user.
    """

    def __init__(
            self,
            username: Optional[str] = None,
            user_id: Optional[int] = None
    ) -> None:
        """
        Initializes the User instance based on username and/or user_id.

        Args:
            username: Assigned by the user through create_username().
            user_id:  The database ID belonging to the username.
        """
        self.username = username
        self.user_id = user_id
        self.habits: List[Habit] = [] # Starts with an empty list of habits

    def create_username(self) -> None:
        """
        Handles the creation of a new username.

        - prompts for user input
        - validates against existing usernames in the database
        - handles confirmation through helper function
        - sets the username attribute if successful, or None if canceled
        """
        # Avoid circular imports
        from db_and_managers.manager_user_db import username_exists

        while True:
            # Ask user for username
            print(f"Please type in your desired username {GRAY}or ENTER << to exit{RES} ")
            username = input().title().strip()

            # Exit the loop if << ENTER
            if not username:
                self.username = None
                return

            # Check if the username already exists (using user db manager function)
            elif username_exists(username):
                print(f"\nUsername '{username}' is taken! Please try again!")
                time.sleep(1)

            # If username is valid
            else:
                # Confirm the choice
                confirmed_username = confirm_input("username", username)

                # If confirmed, set the username and exit the loop
                if confirmed_username is not None:
                    self.username = confirmed_username
                    return
                # If not confirmed (<< ENTER)
                else:
                    return
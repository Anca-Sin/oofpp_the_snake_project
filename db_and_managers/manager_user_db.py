"""
User management database module.

Provides behind the scenes database operations for user related functionality, including:
- loading of users from the db
- user selection
- user creation
- user deletion
"""
import time
from typing import List, Optional

from config import DB_FILEPATH
from core.user import User
from helpers.helper_functions import (db_connection, reload_cli, exit_msg, check_exit_cmd,
                                      setup_header, save_entry_msg, cancel_operation, enter, invalid_input)
from helpers.text_formating import RED, RES, BLUE, GREEN, GRAY


def load_users() -> List[User]:
    """
    Loads all users from the db.

    Returns:
         A list of User objects.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    cursor.execute("SELECT id, username FROM users")
    user_data = cursor.fetchall()

    users = []
    for user_row in user_data:
        user = User(user_id=user_row[0], username=user_row[1])
        users.append(user)

    connection.close()
    return users

def select_user(users: List[User]=None) -> Optional[User]:
    """
    Prompts the user to select an existing user or create a new one if none exists.

    Args:
        users: User objects to be loaded and displayed for choice.
    Returns:
        The selected or newly created User object.
    """
    # If there are no users, directly prompt to create a new user
    if not users:
        while True:
            reload_cli()
            exit_msg()

            print(f"""
                    Welcome to {BLUE}- - - HabitTracker - - -{RES}

                    No users found! You can:

                    1 - Create a {GREEN}new{RES} user
                    2 - Quit the application
                    """)

            choice = input("\n        Enter your choice (1-2): ").strip()

            check_exit_cmd(choice)

            if choice == "1":
                reload_cli()
                setup_header("User")

                selected_user = User()
                selected_user.create_username()

                if not selected_user.username:
                    return None # If user cancels inside create_username()

                save_entry_msg(selected_user.username)
                return selected_user

            elif choice == "2":
                check_exit_cmd("quit")

            else:
                invalid_input()

    # Display the users to choose from
    else:
        while True:
            reload_cli()
            exit_msg()

            print(f"Welcome to {BLUE}- - - HabitTracker - - - {GREEN}(^_^)/{RES}")
            print("\n        Login as: ")
            print("")

            # Display users with numeration
            for idx, user in enumerate(users, 1):
                print(f"        {idx} - {GREEN}{user.username}{RES}")

            # Last option: Create new user
            print("        or")
            print(f"        {len(users) + 1} - Create a {GREEN}new{RES} user")
            print(f"        {len(users) + 2} - Quit the application")

            # Ask user for a choice
            choice = input(f"\n        Enter your choice (1-{len(users) + 1}): ").strip()

            check_exit_cmd(choice)

            try:
                if choice.isdigit() and 1 <= int(choice) <= len(users):
                    selected_user = users[int(choice) - 1]  # Adjust index since user listing starts from 1
                    return selected_user

                elif int(choice) == len(users) + 1:
                    # Create new user
                    reload_cli()
                    setup_header("User")

                    selected_user = User()
                    selected_user.create_username()

                    if not selected_user.username:
                        return None # If user cancels inside create_username()

                    save_entry_msg(selected_user.username) # Helper
                    return selected_user

                elif int(choice) == len(users) + 2:
                    check_exit_cmd("quit")

                else:
                    invalid_input()

            except ValueError:
                invalid_input()

def username_exists(username: str) -> bool:
    """
    Checks if a username already exists in the db.

    Args:
        username: The username to check for.
    Returns:
        True if the username exists, False otherwise.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Count how many rows exist in the 'habits' table
    # where username matches the given value
    cursor.execute("""
        SELECT COUNT(*) FROM users 
        WHERE username = ?
    """, (username,))

    # Returns a tuple with 1 element = the count
    count = cursor.fetchone()[0]

    connection.close()

    return count > 0 # If it exists, returns True, else False

def save_user(user: User) -> None:
    """
    Saves a new user to the db.

    - is only called when creating a new user
    - user_id is updated with the auto-generated ID

    Args:
        user: The User object to save to the db.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Insert new user
    cursor.execute("INSERT INTO users (username) VALUES (?)", (user.username,))
    # Get and set the new user id
    user.user_id = cursor.lastrowid

    connection.commit()
    connection.close()

def delete_user(selected_user) -> None:
    """
    Deletes a user and all associated data from the db.

    - asks for confirmation before deleting

    Args:
        selected_user: The User object to delete.
    """
    # Ask for confirmation
    print(f"""
    {GRAY}---------------------------------------    
    This operation will permanently DELETE:
        
    - Your username '{selected_user.username}'
    - All associated habits and data
    ---------------------------------------{RES}
    """)

    confirmation = input(
        f"Type '{RED}delete{RES}' or {enter()} to cancel: "
    ).lower().strip()

    # Check if the user doesn't confirm
    if confirmation != "delete":
        cancel_operation() # Helper
        return # Return to Main Menu

    # If confirmed, continue with deletion
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # Delete streaks
    cursor.execute("""
        DELETE FROM streaks
        WHERE habit_id IN (
        SELECT id FROM habits WHERE user_id = ?
        )
    """, (selected_user.user_id,))

    # Delete habits
    cursor.execute("DELETE FROM habits WHERE user_id = ?", (selected_user.user_id,))

    # Delete user
    cursor.execute("DELETE FROM users WHERE id = ?", (selected_user.user_id,))

    connection.commit()
    connection.close()

    print(f"\nFarewell, {GREEN}{selected_user.username}{RES}!")
    time.sleep(1)
    print(f"\n{GREEN}(^_^)/ {GRAY}May your tracking continue elsewhere!{RES}")
    time.sleep(1)
    input(f"\n{enter()} to return...")
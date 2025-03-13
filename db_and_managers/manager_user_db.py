import sys
import time
from typing import List

# noinspection PyUnresolvedReferences
from config import DB_FILEPATH

from core.user import User
from helpers.helper_functions import db_connection, reload_cli, exit_msg, reload_menu_countdown, check_exit_cmd
from helpers.colors import RED, RES, BLUE, GREEN, GRAY


def load_users() -> List[User]: # For access to all user properties
    """
    Loads all users from the db.

    :return: A list of User objects.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Query to select all users
    cursor.execute("SELECT id, username FROM users")
    user_data = cursor.fetchall()

    users = []
    for user_row in user_data:
        user = User(user_id=user_row[0], username=user_row[1])
        users.append(user)

    connection.close()
    return users

def select_user(users: List[User]=None) -> User:
    """
    Prompts the user to select an existing user or create a new one if none exists.

    Parameters:
        users: Optional preloaded list of users. If none, users will be loaded.
    Returns:
        The selected or newly created User object.
    """
    # If there are no users, directly prompt to create a new user
    if not users:
        while True:
            reload_cli()
            exit_msg()
            print("""\nNo users found! You can:
        
            1 - Create a new user
            2 - Quit the application
            """)

            choice = input("\nEnter your choice (1-2): ").strip()

            # Check for exit command
            check_exit_cmd(choice)

            if choice == "1":
                selected_user = User()
                selected_user.create_username()
                save_user(selected_user)
                print(f"\nYou've created user: {selected_user.username}!")
                return selected_user
            elif choice == "2":
                print("\n        Exiting the application")
                time.sleep(0.40)
                print("        .")
                time.sleep(0.40)
                print("        .")
                time.sleep(0.40)
                print("        .")
                time.sleep(0.40)
                print(f"\n        Goodbye! {BLUE}(^_^)/{RES}")
                time.sleep(0.40)
                print(f"""
        {BLUE}* * * * * * * * * * * * *{RES}
        {RED}REMEMBER TO STAY ON TRACK{RES}
        {BLUE}* * * * * * * * * * * *{RES}
                """)
                time.sleep(0.40)
                print("        .")
                time.sleep(0.40)
                print("        .")
                time.sleep(0.40)
                print("        .")
                time.sleep(0.40)
                sys.exit(0)
            else:
                print("\nSorry, invalid input. Please try again!")
                reload_menu_countdown()

    # Display the users to choose from
    else:
        while True:
            reload_cli()
            exit_msg()
            # Display users with numeration
            print("")
            print("\n        Login as: ")
            print("")
            for idx, user in enumerate(users, 1):
                print(f"        {idx} - {GREEN}{user.username}{RES}")
            print("        or")
            # Last option: Create new user
            print(f"        {len(users) + 1} - Create a {GREEN}new{RES} user")

            # Ask user for a choice
            choice = input(f"\nEnter your choice (1-{len(users) + 1}): ").strip()

            # Check for exit command
            check_exit_cmd(choice)

            try:
                if choice.isdigit() and 1 <= int(choice) <= len(users):
                    # Confirm the choice
                    selected_user = users[int(choice) - 1]  # Adjust index since user listing starts from 1
                    return selected_user

                elif int(choice) == len(users) + 1:
                    # Create new user
                    selected_user = User()
                    selected_user.create_username()
                    save_user(selected_user)
                    print(f"\nSaving entry to your database...")
                    time.sleep(1)
                    print("")
                    input(f"{GRAY}'{selected_user.username}' Saved! ENTER << to continue...{RES}")
                    return selected_user

                else:
                    print("\nSorry, invalid input. Please try again!")
                    reload_menu_countdown()
            except ValueError:
                print("\nSorry, invalid input. Please try again!")
                reload_menu_countdown()


def username_exists(username: str) -> bool:
    """
    Checks if a username already exists in the db.

    Parameters:
        username: The username to check.
    Returns:
        True if the username exists, False otherwise.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM users 
        WHERE username = ?
    """, (username,))

    count = cursor.fetchone()[0]

    connection.close()
    return count > 0

def save_user(user: User) -> None:
    """
    Saves a new user to the db.
    Doesn't need to check if the user exists because it is called only if there are no users after load_users().

    Parameters:
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
    - deletes on cascade all associated habits and streaks

    Parameters:
        selected_user: The User object to delete.
    """
    # Ask for confirmation
    print(f"""This operation will permanently DELETE:
        
    - Your username
    - All associated habits and data
    """)

    confirmation = input(f"Type in '{RED}DELETE{RES}' if you are sure to proceed {GRAY}(or cancel by pressing ENTER){RES}: ")

    # Check if the user doesn't confirm
    if confirmation.lower() != "delete":
        print("\nDeletion canceled.")
        reload_menu_countdown()
        return # Return to Main Menu

    # If confirmed, continue with deletion
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

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

    print(f"\nUser '{RED}{selected_user.username}{RES}' and all associated data have been {RED}deleted{RES}.")
    reload_menu_countdown()
import sys
from typing import List

# noinspection PyUnresolvedReferences
from config import DB_FILEPATH

from core.user import User
from helpers.helper_functions import *

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
        user = User(user_id=user_data[0], username=user_row[1])
        users.append(user)

    connection.close()
    return users

def select_user() -> User:
    """
    Prompts the user to select an existing user or create a new one if none exists.

    :return: The selected or newly created User object.
    """
    # Load all users
    users = load_users()

    # If there are no users, directly prompt to create a new user
    if not users:
        while True:
            reload_cli()
            print("""No users found! You can:
        
            1. Create a new user
            2. Quit the application
            """)

            choice = input("\nEnter your choice (1-2): ").strip()

            if choice == "1":
                selected_user = User()
                selected_user.create_username()
                save_user(selected_user)
                return selected_user
            elif choice == "2":
                sys.exit() # Close the app
            else:
                print("\nSorry, invalid input. Please try again!")
                reload_menu_countdown()

    # Display the users to choose from
    else:
        while True:
            reload_cli()
            # Display users with numeration
            print("Please select a user from the following list: ")
            for idx, user in enumerate(users, 1):
                print(f"{idx}. {user.username}")

            # Ask user for a choice
            choice = input(f"Enter your choice (1-{len(users)}): ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(users):
                # Confirm the choice
                confirmed_choice = confirm_int_input(choice)

                # If the choice was confirmed, get the corresponding user
                selected_user = users[int(confirmed_choice) - 1]  # Adjust index since user listing starts from 1
                print(f"You've selected: {selected_user.username}")
                return selected_user

            else:
                print("\nSorry, invalid input. Please try again!")
                reload_menu_countdown()

def save_user(user: User) -> None:
    """
    Saves a user to the db.
    Doesn't need to check if the user exists because it is called only if there are no users after load_users().

    :param user: The User object to save.
    :return: The user_id from the db.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Insert new user
    cursor.execute("INSERT INTO users (username) VALUES (?)", (user.username,))
    connection.commit()

    connection.close()

def delete_user(selected_user) -> None:
    """Deletes an user and all associated data."""
    # Ask for confirmation
    print(f"""This operation will permanently DELETE:
        
    - Your username
    - All associated habits and data

    """)

    confirmation = input("Type in 'DELETE' if you are sure to proceed (or cancel by pressing ENTER): ")

    if confirmation.lower() != "delete":
        print("Deletion canceled.")
        reload_menu_countdown()
        return # To the main menu

    # If not canceled, continue with deletion
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Delete the user - cascading will delete its associated data
    cursor.execute("DELETE FROM users WHERE username = ?", (selected_user.username,))

    connection.commit()
    connection.close()

    print(f"User '{selected_user.username}' and all associated data have been deleted.")
    reload_menu_countdown()
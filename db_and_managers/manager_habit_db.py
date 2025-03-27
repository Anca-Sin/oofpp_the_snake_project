"""
Habit management database module.

Provides behind the scenes database operations for habit related functionality, including:
- loading of habits from the db
- saving of habits and their implicit properties (completions, streaks,etc.)
- habit creation
- habit deletion
"""

from typing import List, Optional
from datetime import datetime

from config import DB_FILEPATH
from core.habit import Habit
from core.streaks import Streaks
from core.user import User
from helpers.text_formating import RED, RES, GRAY
from helpers.helper_functions import db_connection, reload_menu_countdown, save_entry_msg, cancel_operation, enter


def load_habits(selected_user: User) -> List[Habit]:
    """
    Loads all habits for the selected user from the db.

    - retrieves habit records
    - converts them to Habit objects
    - loads completion dates and streak information

    Args:
        selected_user: The User object whose habits to load.
    Returns:
        List of Habit objects for the selected user.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, user_id, habit_name, frequency, creation_date,
            completions_count, completion_dates
        FROM habits 
        WHERE user_id = ?
    """, (selected_user.user_id,))

    habit_data = cursor.fetchall()

    # List to hold Habit objects
    habits = []

    # Process each habit record from the db
    for habit_row in habit_data:
        habit_id = habit_row[0]

        # Habit object information
        habit = Habit()
        habit.name = habit_row[2]
        habit.frequency = habit_row[3]

        # Convert creation date to datetime.date object
        habit.creation_date = datetime.strptime(habit_row[4], "%Y-%m-%d").date()

        # Load completion dates
        completion_dates = habit_row[6]
        habit.completion_dates = []
        if completion_dates:
            # Convert comma separated string of dates to list of date objects
            habit.completion_dates = [
                datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
                for date_str in completion_dates.split(",")
            ]

        # Initialize streaks
        habit.streaks = Streaks()

        # Load streak data
        cursor.execute("""
            SELECT current_streak, longest_streak, streak_length_history
            FROM streaks
            WHERE habit_id = ?
        """, (habit_id,))

        streak_data = cursor.fetchone()

        if streak_data:
            # Streak information
            habit.streaks = Streaks()
            habit.streaks.current_streak = streak_data[0] or 0 # Default to 0 if None
            habit.streaks.longest_streak = streak_data[1] or 0

            # Load broken streak history
            streak_history = streak_data[2]
            if streak_history and streak_history.strip():
                # Convert comma separated string to list on integers
                habit.streaks.broken_streak_lengths = [int(streak) for streak in streak_history.split(",")]

        # Add to the list
        habits.append(habit)

    connection.close()
    return habits


def habit_name_exists(selected_user: User, habit_name: str) -> bool:
    """
    Checks if a habit name already exists for the selected user.

    Args:
        selected_user: The User object to check habits for.
        habit_name: The habit name to check.
    Returns:
         True if the habit name exists for the user, False otherwise.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Count how many rows exist in the 'habits' table
    # where both user_id and habit_name match the given values
    cursor.execute("""
        SELECT COUNT(*) FROM habits
        WHERE user_id = ? AND habit_name = ?
    """, (selected_user.user_id, habit_name))

    # Returns a tuple with 1 element = the count
    count = cursor.fetchone()[0]

    connection.close()

    return count > 0 # If it exists, returns True, else False

def new_habit(selected_user: User, set_frequency: str = None) -> Optional[Habit]:
    """
    Creates a new habit for the selected user.

    - creates a new Habit object
    - prompts the user for habit details (or uses preset values)

    Args:
        selected_user: The User object to associate the new habit with.
        set_frequency: Optional preset frequency ("daily" or "weekly") to use
                       when accessed from list "daily" or "weekly" and no habits exist.
    Returns:
        The new Habit object or None if creation is canceled.
    """
    # Create a new Habit object
    habit = Habit()

    # Habit naming method
    habit.habit_name(selected_user)

    # Check if user wants to exit during habit naming
    if habit.name is None:
        return None

    # Habit frequency method
    # Uses preset if called from weekly/daily
    habit.habit_frequency(preset_frequency=set_frequency)
    habit.create_date()

    # Check if user wants to exit during frequency setting:
    if habit.frequency is None:
        return None

    save_entry_msg(habit.name) # Helper
    return habit

def save_habits(selected_user: User, new_habit: Habit = None) -> None:
    """
    Saves (INSERT) / Updates (UPDATE) habit data in the db.

    Args:
        selected_user: The User object whose habits to save/update.
        new_habit: INSERT The new Habit object to the db and initialises all its attributes
                   UPDATE If None -> used in completion manager, where
                                     habit: Habit is passed as parameter in the completions functions
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    if new_habit:
        # Insert the new habit
        cursor.execute("""
            INSERT INTO habits (user_id, habit_name, frequency, creation_date,
            completions_count, completion_dates)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            selected_user.user_id,
            new_habit.name,
            new_habit.frequency,
            new_habit.creation_date.strftime("%Y-%m-%d"),
            0,  # Initialize completion counts as 0
            ""  # Initialize completion_dates as an empty string
        ))

        # Get the auto-generated habit ID
        habit_id = cursor.lastrowid

        # Initialize streak record
        cursor.execute("""
            INSERT INTO streaks (habit_id, current_streak, longest_streak, streak_length_history)
            VALUES (?, ?, ?, ?)
        """, (
            habit_id,
            0,  # Initialize current_streak as 0
            0,  # Initialize longest_streak as 0
            ""  # Initialize streak history as an empty string
        ))

    else:
        # Update existing habits
        for habit in selected_user.habits:
            cursor.execute("""
                UPDATE habits
                SET completions_count = ?, completion_dates = ?
                WHERE user_id = ? AND habit_name = ?
            """, (
                len(habit.completion_dates), # Update number of completions
                ",".join(completion_date.strftime("%Y-%m-%d") for completion_date in habit.completion_dates)
                    if habit.completion_dates else "", # Update completion dates
                selected_user.user_id,
                habit.name
            ))

            cursor.execute("""
                UPDATE streaks
                SET current_streak = ?, longest_streak = ?, streak_length_history = ?
                WHERE habit_id = (SELECT id FROM habits WHERE user_id = ? AND habit_name = ?)
            """, (
                habit.streaks.current_streak,
                habit.streaks.longest_streak,
                # Convert broken_streak_lengths list to a comma separated string
                ",".join(map(str, habit.streaks.broken_streak_lengths)) if habit.streaks.broken_streak_lengths else "",
                selected_user.user_id,
                habit.name
            ))

    connection.commit()
    connection.close()

def delete_habit(selected_user: User, habit: Habit) -> None:
    """
    Deletes a habit and all associated data from the db.

    - asks for confirmation before deleting

    Args:
        selected_user: The User object whose habit to delete.
        habit: The Habit object to delete.
    """
    # Ask for confirmation
    print(f"""
        {GRAY}---------------------------------------
        This operation will permanently DELETE:

        - Your '{habit.name}' habit
        - All associated habit data
        ---------------------------------------{RES}
    """)

    confirmation = input(
        f"        Type in '{RED}delete{RES}' or {enter()} to cancel: "
    ).lower().strip()

    # Check if the user doesn't confirm
    if confirmation != "delete":
        cancel_operation() # Helper
        return  # To the Habit Detail Menu

    # If confirmed, continue with deletion
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Find the habit ID
    cursor.execute("""
        SELECT id FROM habits
        WHERE user_id = ? AND habit_name = ?
    """, (selected_user.user_id, habit.name))

    habit_id = cursor.fetchone()[0]

    # Delete streaks
    cursor.execute("DELETE FROM streaks WHERE habit_id = ?", (habit_id,))

    # Delete habit
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

    connection.commit()
    connection.close()

    input(f"\n'{RED}{habit.name}' has been thrown {RED}off your track{RES}! {enter()} to return...")
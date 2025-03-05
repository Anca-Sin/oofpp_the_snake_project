from typing import List
from datetime import datetime

from config import DB_FILEPATH

from core.habit import Habit
from core.streaks import Streaks
from helpers.helper_functions import db_connection

def load_habits(selected_user) -> List[Habit]:
    """
    Loads all habits for the selected user.

    :param selected_user: The User objects whose habits to load.
    :return: A list of Habit objects.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Get habits for the selected user
    cursor.execute("""
        SELECT id, user_id, habit_name, frequency, creation_date,
            completions_count, check_off_dates
        FROM habits 
        WHERE user_id = ?
    """, (selected_user.user_id,))

    habit_data = cursor.fetchall()
    habits = [] # List to hold Habit objects

    for habit_row in habit_data:
        habit_id = habit_row[0]
        habit = Habit()
        habit.name = habit_row[2]
        habit.frequency = habit_row[3]
        # Convert creation date to datetime.date object
        habit.creation = datetime.strptime(habit_row[4], "%Y-%m-%d").date()

        # Load completion dates
        checked_off_dates = habit_row[6]
        habit.completion_dates = []
        if checked_off_dates:
            habit.completion_dates = [
                datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
                for date_str in checked_off_dates.split(",")
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
            habit.streaks = Streaks()
            habit.streaks.current_streak = streak_data[0] or 0 # Default to 0 if None
            habit.streaks.longest_streak = streak_data[1] or 0
            # Load broken streak history
            streak_history = streak_data[2]
            if streak_history and streak_history.strip():
                habit.streaks.broken_streak_length = [int(streak) for streak in streak_history.split(",")]

        habits.append(habit)

    connection.close()
    return habits

def new_habit(selected_user, habit: Habit) -> None:
    """
    Adds a new habit to the user's db.

    :param selected_user: The User object to associate the habit with.
    :param habit: The Habit object to add.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    habit = Habit()
    habit.habit_name()
    habit.habit_frequency()
    habit.creation_date()

    # Format creation date for storage
    creation_date_str = habit.creation.strftime("%Y-%m-%d")

    # Convert completion dates to a comma-separated
    # Insert the habit
    cursor.execute("""
        INSERT INTO habits (user_id, habit_name, frequency, creation_date,
        completions_count, checked_off_dates)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        selected_user.user_id,
        habit.name,
        habit.frequency,
        creation_date_str,
        0, # Initialize completion counts as 0
        "" # Initialize check_off_dates as an empty string
    ))

    # Get the habit ID
    habit_id = cursor.lastrowid

    # Initialize streak record
    cursor.execute("""
        INSERT INTO streaks (habit_id, current_streak, longest_streak, streak_length_history)
        VALUES (?, ?, ?, ?)
    """, (
        habit_id,
        0, # Initialize current_streak as 0
        0, # Initialize longest_streak as 0
        "" # Initialize streak history as an empty string
    ))

    connection.commit()
    connection.close()

def save_habits(selected_user) -> None:
    """
    Saves all habits for a user to the db.

    :param selected_user: The User object whose habits to save/update.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # For each habit in the user's habit list
    for habit in selected_user.habits:
        # Check if the habit already exists
        cursor.execute("""
            SELECT id FROM habits
            WHERE user_id = ? AND habit_name =?
        """, (selected_user.user_id, habit.name))

        result = cursor.fetchone()

        if result:
            # If the habit exists, update it
            habit_id = result[0]
            cursor.execute("""
                UPDATE habits
                SET completions_count = ?, checked_off_dates = ?
                WHERE id = ?
            """, (
                len(habit.completion_dates), # Update number of completions
                ",".join(completion_date.strftime("%Y-%m-%d") for completion_date in habit.completion_dates)
                    if habit.completion_dates else "", # Update completion dates
                habit_id
            ))

            # Update streak data including broken streak history
            # Convert broken_streak_length list to a comma separated string
            streak_history = ""
            if habit.streaks.broken_streak_length:
                streak_history = ",".join(map(str, habit.streaks.broken_streak_length))

            cursor.execute("""
                UPDATE streaks
                SET current_streak = ?, longest_streak = ?, streak_length_history = ?
                WHERE habit_id = ?
            """, (
                habit.streaks.current_streak,
                habit.streaks.longest_streak,
                streak_history,
                habit_id
            ))

        else:
            # Insert new habit
            new_habit(selected_user, habit)

    connection.commit()
    connection.close()

def delete_habit(selected_user, habit: Habit) -> None:
    """
    Deletes a habit and its associated data from the db.

    :param selected_user: The User object whose habit to delete.
    :param habit: The Habit object to delete.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Find the habit ID
    cursor.execute("""
        SELECT id FROM habits
        WHERE user_id = ? AND habit_name = ?
    """, (selected_user.user_id, habit.name))

    habit_id = cursor.fetchone()[0]

    # Delete all information, including streaks, on cascade
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

    connection.commit()
    connection.close()
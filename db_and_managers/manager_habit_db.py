from typing import List
from datetime import datetime

from config import DB_FILEPATH

from core.habit import Habit
from core.streaks import Streaks
from helpers.helper_functions import db_connection

"""
add habit
load habits
save habits
delete habit
"""

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
    habits = []

    for habit_row in habit_data:
        habit_id = habit_row[0]
        habit = Habit()
        habit.name = habit_row[2]
        habits.append(habit)
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

        # Load streak data
        cursor.execute("""
            SELECT current_streak, longest_streak, streak_length_history
            FROM streaks
            WHERE habit_id = ?
        """, (habit_id,))

        streak_data = cursor.fetchone()
        if streak_data:
            habit.streaks = Streaks(selected_user.db)
            habit.streaks.current_streak = streak_data[0] or 0
            habit.streaks.longest_streak = streak_data[1] or 0

        habits.append(habit)

    connection.close()
    return habits

def add_habit(selected_user, habit: Habit) -> None:
    """
    Adds a new habit to the user's db.

    :param selected_user: The User object to associate the habit with.
    :param habit: The Habit object to add.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Format creation date for storage
    creation_date_str = habit.creation.strftime("%Y-%m-%d")

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
        len(habit.completion_dates),
        ",".join(completion_date.strftime("%Y-%m-%d") for completion_date in habit.completion_dates)
        if habit.completion_dates else ""
    ))

    # Get the habit ID
    habit_id = cursor.lastrowid

    # Initialize streak record
    cursor.execute("""
        INSERT INTO streaks (habit_id, current_streak, longest_streak, streak_length_history)
        VALUES (?, ?, ?, ?)
    """, (
        habit_id,
        habit.streaks.current_streak,
        habit.streaks.longest_streak,
        ""
    ))

    connection.commit()
    connection.close()
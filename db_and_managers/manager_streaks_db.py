from config import DB_FILEPATH

from helpers.helper_functions import db_connection

def load_broken_streak_length(habit_name: str) -> str:
    """
    Loads streak_length_history for a given habit from the db.
    Streak_length_history is initialized as an empty string when creating a habit,
    so will always return a valid string.

    :param habit_name: The name of the habit.
    :return: The broken streaks' lengths as a comma separated string.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Retrieve the streak_length_history for the given habit
    cursor.execute("""
        SELECT streak_length_history
        FROM streaks
        JOIN habits ON streaks.habit_id = habit.id
        WHERE habits.habit_name = ?
    """, (habit_name,))

    result = cursor.fetchone()
    connection.close()

    return result[0] # Will return empty string if no history
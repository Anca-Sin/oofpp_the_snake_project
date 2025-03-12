from config import DB_FILEPATH

from helpers.helper_functions import db_connection

def load_broken_streak_lengths(habit_name: str) -> str:
    """
    Loads streak_length_history for a given habit from the db.

    - retrieves the history of broken streak lengths for a selected habit
    - streak_length_history is initialized as an empty string when creating a habit,
      so it will always return a valid string

    Parameters:
        habit_name: The name of the habit to get the streak history for.
    Returns:
        The broken streaks' lengths as a comma separated string.
        An empty string if no history exists.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Retrieve the streak_length_history for the selected habit
    cursor.execute("""
        SELECT streak_length_history
        FROM streaks
        JOIN habits ON streaks.habit_id = habits.id
        WHERE habits.habit_name = ?
    """, (habit_name,))

    # Get result
    result = cursor.fetchone()
    connection.close()

    # Will return empty string if no history
    return result[0]
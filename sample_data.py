"""
Sample Data Generator for Habit Tracker

Creates a sample user and 5 predefined habits (3 daily, 2 weekly) with 4 weeks of training data.

- checks for existing sample user
    - if it exists, skips the creation process
- checks for existing sample habits
    - if they exist, skips the creation process
- uses existing project functions for habit completion generation and streak calculation
"""

import random
from datetime import datetime, timedelta, date
from typing import List

from core.streaks import Streaks
from core.user import User
from core.habit import Habit
from db_and_managers.database import Database


def _generate_completions(habit: Habit, start_date: date, end_date: date) -> List[date]:
    """Generates random completions for sample data with proper streak calculation"""
    # Reset habit data
    habit.completion_dates = []
    habit.streaks = Streaks()
    habit.streaks.current_streak = 0
    habit.streaks.longest_streak = 0
    habit.streaks.broken_streak_length = []

    completions = []
    current_date = start_date
    last_week_completion = None

    while current_date <= end_date:
        # Determine if habit should be completed on this date (random probability)
        if habit.frequency == "daily":
            if random.randint(1, 10) <= 8:  # 80% chance
                # Check-off the habit as completed for the date
                habit.check_off_habit(current_date)
                completions.append(current_date)


        elif habit.frequency == "weekly":
            week_start = current_date - timedelta(days=current_date.weekday())
            if last_week_completion is None or week_start != last_week_completion:
                if random.randint(1, 10) <= 9:  # 90% chance
                    # Check-off the habit as completed for the date
                    habit.check_off_habit(current_date)
                    completions.append(current_date)
                    last_week_completion = week_start

        # Move to next day
        current_date += timedelta(days=1)

    return completions

def sample_data_generator():
    """Creates a sample user and 5 predefined habits with 4 weeks of completion data."""
    # Initialize Database
    db = Database()

    # Load existing users
    existing_users = db.load_users()
    # Check if sample user exists
    sample_user = next((user for user in existing_users if user.username == "SampleUser"), None)

    # If sample user exists
    if sample_user:
        print("Skipping... 'SampleUser' already exists...")
    else:
        # If not, start creating one
        sample_user = User(username="SampleUser")
        # Add to db
        db.save_user(sample_user)
        print("Created 'SampleUser'!")

    # Predefine 5 sample habits
    sample_habits = [
        {"name": "Morning Meditation", "frequency": "daily"},
        {"name": "Read 30 Minutes", "frequency": "daily"},
        {"name": "Drink 2L Water", "frequency": "daily"},
        {"name": "Weekly Planning", "frequency": "weekly"},
        {"name": "Deep House Cleaning", "frequency": "weekly"}
    ]

    # Load existing habits
    db.load_habits(sample_user)
    existing_habit_names = [habit.name for habit in sample_user.habits]

    for habit_info in sample_habits:
        # If sample habit names exist
        if habit_info["name"] in existing_habit_names:
            print(f"Skipping... Habit '{habit_info['name']}' already exists...")
        else:
            # Create new sample habit
            new_habit = Habit()
            new_habit.name = habit_info["name"]
            new_habit.frequency = habit_info["frequency"]
            new_habit.creation_date()
            # Add to db
            db.save_habits(sample_user, new_habit)
            print(f"Created sample habit '{habit_info['name']}'!")

    # Reload existing habits
    db.load_habits(sample_user)

    # Calculate date range for 4 weeks of data
    end_date = datetime.now().date()           # Today
    start_date = end_date - timedelta(days=28) # 4 weeks ago

    # Process each habit
    for habit in sample_user.habits:
        # Only process our sample habits
        if habit.name not in [h["name"] for h in sample_habits]:
            continue

        else:
            print(f"\nGenerating completions for '{habit.name}'...")

            # Generate completions using helper function
            habit.completion_dates = _generate_completions(habit, start_date, end_date)
            print(f"\nHabit: {habit.name}")
            print(f"Completions: {habit.completion_dates}")
            print(f"Current Streak: {habit.streaks.current_streak}")
            print(f"Longest Streak: {habit.streaks.longest_streak}")
            print(f"Broken Streaks Lengths: {habit.streaks.broken_streak_length}")
            # Count completions
            completions = habit.completion_dates
            completion_count = len(completions)

            # Show completions count for each sample habit
            if habit.frequency == "daily":
                print(f">> ... for 'daily': added {completion_count} new random completions!")
            elif habit.frequency == "weekly":
                print(f">> ... for 'weekly': added {completion_count} new random completions!")

            # Save the newly generated completions to the db
            db.save_habits(sample_user)

def instructions():
    print("""
    Sample data created successfully:
    - 5 habits with 4 weeks of randomly generated completion data
    - streak information has been calculated
    - login as 'SampleUser' to explore the data
    """)

if __name__ == "__main__":
    sample_data_generator()
    instructions()
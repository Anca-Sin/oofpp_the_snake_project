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
from datetime import datetime, timedelta

from core.user import User
from core.habit import Habit
from db_and_managers.database import Database

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
        print("Sample user already exists. Skipping...")
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
            print(f"Habit '{habit_info['name']}' already exists. Skipping...")
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
            print(f"Generating completions for '{habit.name}'...")

            # Always generates new random completions
            # Need to clear existing completions and reset streak data
            habit.completion_dates = []
            habit.streaks.current_streak = 0
            habit.streaks.longest_streak = 0
            habit.streaks.broken_streak_length = []

            # Save the reset data to the db
            db.save_habits(sample_user)

            # Generate completion dates for the 4 weeks period
            # Start from 4 weeks ago
            current_date = start_date
            # Start from a clean slate
            completion_count = 0

            # Loop through each day in the 4 weeks period
            while current_date <= end_date:
                # should_complete: bool -> determines if we complete the habit for the day
                # Initially set to False (not completed)
                should_complete = False

                # Determine if habit should be completed on this date
                # Using random probabilities to simulate completion patterns
                # 1-8 = "complete the habit" (80% chance)
                # 9-10 = "skip the habit"    (20% chance)
                if habit.frequency == "daily":
                    # 80% completions
                    should_complete = random.randint(1, 10) <= 8
                elif habit.frequency == "weekly":
                    # 90% completion
                    should_complete = random.randint(1, 10) <= 9

                # If the random check passed, add a completion for this date
                if should_complete:
                    # Complete the habit for this date (updates all changes)
                    _add_past_completion(db, sample_user, habit, current_date)
                    completion_count += 1

                # Move to the next day
                current_date += timedelta(days=1)

            print(f"Added {completion_count} completions for '{habit.name}'!")

print("""\nSample data created successfully:
- 5 habits with 4 weeks of randomly generated completion data
- streak information has been calculated
- login as 'SampleUser' to explore the data
""")

def _add_past_completion(db, user, habit, completion_date):
    """
    Adds a completion for a specific past date.
    No user input and cli - can't reuse already defined methods.

    - adds the completion date to the habit's completion_dates list
    - updates streak calculations based on the new completion
    - saves the updated habit and streak data to the db

    Parameters:
        db: Database instance for saving data -> inherited inside create_sample_data().
            => Not reopening a database instance each time a date is added.
        user: The User object whose habit we complete.
        habit: The Habit object to complete.
        completion_date: Date to mark as completed.
    """
    # No need to check if already completed - each date is only processed once

    # Add completion to the habit's completions list
    habit.completion_dates.append(completion_date)

    # Update streak information
    # Calculates current streak, handles longest_streak and broken_streak_length
    habit.streaks.get_current_streak(habit.frequency, habit.completion_dates)

    # Save changes to the db
    db.save_habits(user)

if __name__ == "__main__":
    sample_data_generator()
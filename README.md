# The Snake Project
My first coding project! A habit tracker app created for the Object Oriented and Functional Programming with Python course.

---

# Project Overview and Features

- command-line interface with consistent styling and **Wavey McTrackface** *(the personal habit-tracking sidekick!)*
- object-oriented design principles 
- functional programming for analytics
- supports multiple users (no login required)
- user deletion
- creation of daily and weekly habits
- habit deletion
- daily completion, retroactive completion, and deletion
- calendar view with navigation options
- analytics:
	- across all habits
	- filtered by frequency
	- for a selected habit
- current analytics implementations:
	- filtering habits by periodicity
	- listing all habits
	- current and longest streak across all habits, by frequency, for selected habit
	- most and least completed habits across all habits, by frequency, for selected habit
	- average streak length across all habits, by frequency, for selected habit
- intuitive menu progression from general to specific
- consistent screen reloading between menus, back and quit options
- consistent input confirmation and error handling
- unit testing for core classes
- unit testing for submission sample data
---

# Future Development Perspectives Supported by the Current Architecture

## Advanced habit metrics
- habit/username editing
- habit prioritization system (show highest completed first)
- extended analytics such as:
	- success rate % with trend analysis
	- completion rates comparison by average
	- time pattern analysis
	- data filtering by date ranges

## Additional frequencies
- monthly, quarterly
- custom frequency set by the user
## Enhancing cli features:
- command shortcuts
- streak graphs or charts
- progress bar for streak counts

---
		
# Getting Started

## Requirements
- Python 3.7+ 
- SQLite (included in Python standard library)
- pip

## Usage
1. Clone the repository: 
```
git clone https://github.com/Anca-Sin/oofpp_the_snake_project.git
```
2. Navigate to the project directory: 
```
cd oofpp_the_snake_project
```
3. Run the app: 
```
python main.py
```
4. Testing:
- Core Classes
```
python unit_tests_core_classes.py
```
- Submission Sample Data
```
python unit_tests_sample_data.py
```
5. [Optional] Generate more sample data
!!! Running this will overwrite submission sample data completions and affect submission sample testing module !!!
```
python sample_data.py
```
---

# Project Structure:
```
oofpp_the_snake_project/
├── main.py                      # App entry point, initializes database and user selection/creation
├── sample_data.py               # Sample data generator
├── config.py                    # Config settings for db connection
├── unit_tests_core_classes.py   # Unittest for core classes
├── unit_tests_sample_data.py    # Unittest for submission sample data
├── habit_tracker.db             # SQLite db file
│
├── cli/                         # Command-line interface menus
│   ├── calendar_view.py         # Calendar menu with navigation and completion/deletion options
│   ├── main_menu.py             # Main menu after user selection
│   ├── menu_analytics.py        # Analytics menu across all habits and by frequency
│   ├── menu_habit_details.py    # Selected habit menu
│   ├── menu_habits.py           # General habit menu with creation, deletion, habit listing
│   └── menu_my_habit_tracker.py # My habit tracker menu
│
├── core/                        # Core classes
│   ├── analytics.py             # Analytics using FP & user dependency injection
│   ├── habit.py                 # Handles all habit operations, initializes streaks
│   ├── streaks.py               # Subclass to habit, handles complex streak logic
│   └── user.py                  # Handles user creation, contains a list of Habits
│
├── db_and_managers/             # Database management
│   ├── database.py              # Database class with wrapper methods
│   ├── db_structure.py          # Database tables
│   ├── manager_completion_db.py # Handles completions logic and user interactions
│   ├── manager_habit_db.py      # Handles habit-related logic and user interactions
│   └── manager_user_db.py       # Handles user-related logic, user interactions, and acts as the user selection menu
│
└── helpers/                     # Utility functions
    ├── helper_functions.py      # All reusable functions from db connection to cli styling
    └── text_formatting.py       # Simple color schema and text formatting
```

---

# Acknowledgements:
Special thanks to my tutor!  (^_^)/
The book "Python Crash Course" by Erik Matthes helped me make those first baby-steps.

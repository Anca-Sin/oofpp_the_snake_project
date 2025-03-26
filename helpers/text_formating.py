"""
Text formating constants for terminal text formatting.

This module provides ANSI color codes for consistent terminal output styling throughout the application.
"""
from tkinter.font import ITALIC

# Base colors
BLUE = "\033[34m"   # Used for headers and titles
RED = "\033[91m"    # Used for warnings, errors, and deletions
GREEN = "\033[92m"  # Used for users, success messages and confirmations

# Additional formatting
GRAY = "\033[90m"   # Used for secondary information and hints
RES = "\033[0m"     # Resets formatting to terminal default

# Italic
ITAL = "\033[3m"

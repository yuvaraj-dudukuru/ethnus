#!/usr/bin/env python
# Docstring indicating this is Django's command-line utility for administrative tasks
"""Django's command-line utility for administrative tasks."""
# Import os module to interact with the operating system
import os
# Import sys module to pass command line arguments
import sys


# Define the main function that runs when the script is executed
def main():
    # Docstring explaining the purpose of the main function
    """Run administrative tasks."""
    # Set the default settings module environment variable so Django knows where settings.py is located
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campushub.settings')
    try:
        # Try importing the execute_from_command_line function to run the command
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If the import fails (e.g., Django is not installed), raise an error explaining the issue
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command passed via sys.argv (like runserver, makemigrations, etc.)
    execute_from_command_line(sys.argv)


# Python idiom to execute main() only if the script is run directly (not imported)
if __name__ == '__main__':
    # Call the main function
    main()

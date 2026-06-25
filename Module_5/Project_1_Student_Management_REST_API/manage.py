#!/usr/bin/env python
# ============================================================================
#  manage.py — Django's command-line control panel
# ----------------------------------------------------------------------------
#  This is the file you run from the terminal to do EVERYTHING with the
#  project. You never edit it; you just call it, for example:
#
#       python manage.py runserver        -> start the website
#       python manage.py migrate          -> build the database tables
#       python manage.py makemigrations   -> record changes to the models
#       python manage.py createsuperuser  -> create an admin login
#       python manage.py seed             -> (our custom command) load sample data
#
#  Django auto-generated this file; the only line that matters to us is the
#  one that tells Django WHERE the settings live (campushub.settings).
# ============================================================================
import os
import sys


def main():
    """Run administrative tasks."""
    # Tell Django which settings file to use. "campushub" is the project
    # folder, "settings" is the settings.py module inside it.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campushub.settings')
    try:
        # Pull in Django's command runner.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If this fails, Django is not installed in the active environment.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Hand whatever you typed after "manage.py" over to Django to execute.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

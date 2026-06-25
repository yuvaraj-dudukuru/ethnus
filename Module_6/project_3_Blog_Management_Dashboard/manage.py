#!/usr/bin/env python
# ============================================================================
#  manage.py — Django's command-line control panel
# ----------------------------------------------------------------------------
#  Run this from the terminal to do EVERYTHING with the project, for example:
#
#       python manage.py runserver        -> start the website
#       python manage.py migrate          -> build the database tables
#       python manage.py makemigrations   -> record changes to the models
#       python manage.py seed             -> (our custom command) load sample data
#       python manage.py test             -> run the automated tests
#
#  The only line that matters to us tells Django WHERE the settings live
#  (bloghub.settings).
# ============================================================================
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloghub.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

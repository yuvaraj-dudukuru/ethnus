# ============================================================================
#  pagination.py — how long lists are broken into pages
# ----------------------------------------------------------------------------
#  Without pagination, asking for /api/students/ would dump ALL students in
#  one giant response. That is slow and wasteful. Instead we return them in
#  small "pages" and give the client links to the next/previous page.
#
#  This is the StandardPagination referenced in settings.py under
#  'DEFAULT_PAGINATION_CLASS'.
# ============================================================================
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10                  # show 10 items per page by default
    page_size_query_param = 'page_size'  # client may override, e.g. ?page_size=25
    max_page_size = 50              # but never allow more than 50 at once

# Example requests once this is active:
#   GET /api/students/?page=2          -> the second page of 10 students
#   GET /api/students/?page_size=25    -> 25 students per page instead of 10

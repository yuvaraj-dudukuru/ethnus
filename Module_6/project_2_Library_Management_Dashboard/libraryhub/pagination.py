# ============================================================================
#  pagination.py — how long lists are broken into pages
# ----------------------------------------------------------------------------
#  Instead of dumping every book/issue in one giant response, the API returns
#  them in small "pages" with links to the next/previous page. This is the
#  StandardPagination referenced in settings.py.
# ============================================================================
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10                       # show 10 items per page by default
    page_size_query_param = 'page_size'  # client may override, e.g. ?page_size=25
    max_page_size = 50                   # but never allow more than 50 at once

# Examples:
#   GET /api/books/?page=2          -> the second page of 10 books
#   GET /api/books/?page_size=25    -> 25 books per page instead of 10

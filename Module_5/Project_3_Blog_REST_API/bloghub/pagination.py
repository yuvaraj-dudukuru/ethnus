# ============================================================================
#  pagination.py — how long lists are broken into pages
# ----------------------------------------------------------------------------
#  Instead of dumping every post in one giant response, the API returns them
#  in small "pages" with links to the next/previous page.
# ============================================================================
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10                       # 10 items per page by default
    page_size_query_param = 'page_size'  # client may override, e.g. ?page_size=25
    max_page_size = 50                   # but never more than 50 at once

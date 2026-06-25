# ============================================================================
#  pagination.py — how long lists are broken into pages
# ----------------------------------------------------------------------------
#  Instead of dumping every job/application in one response, the API returns
#  them in small "pages" with links to the next/previous page.
# ============================================================================
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

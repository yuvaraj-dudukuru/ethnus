# ============================================================================
#  pagination.py — the project-wide default paging style
# ----------------------------------------------------------------------------
#  This simple "page number" style (?page=2) is used for most lists, like
#  orders. The PRODUCT catalog uses a different style — CursorPagination —
#  defined in shop/pagination.py, because a big live catalog changes while
#  people are browsing and cursor paging stays correct.
# ============================================================================
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

# ============================================================================
#  pagination.py (shop app) — CursorPagination for the product catalog
# ----------------------------------------------------------------------------
#  WHY CURSOR PAGINATION FOR PRODUCTS?
#  A normal ?page=2 (offset) breaks on a big, LIVE catalog: if someone adds or
#  removes a product while you're browsing, items can shift between pages and
#  you might see duplicates or skips. CursorPagination instead pages from a
#  fixed point ("everything after this product"), so it stays correct even
#  while the catalog changes. It gives "next"/"previous" links instead of
#  page numbers.
# ============================================================================
from rest_framework.pagination import CursorPagination


class ProductCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created'          # must match a stable, ordered field on Product
    cursor_query_param = 'cursor'  # the URL parameter that holds the cursor

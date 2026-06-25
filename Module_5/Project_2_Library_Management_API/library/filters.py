# ============================================================================
#  filters.py — defines the ?query=parameters clients can filter books by
# ----------------------------------------------------------------------------
#  Works together with DjangoFilterBackend (switched on in api_views.py).
#  Examples:
#     /api/books/?available=true   -> only books with a free copy
#     /api/books/?author=3         -> only books by author #3
#     /api/books/?search=python    -> (handled by SearchFilter) title/isbn match
# ============================================================================
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    # 'available' is not a real column (is_available is a @property, which the
    # database can't filter on directly). So we write a CUSTOM method filter:
    # when the client passes ?available=true we translate it into the database
    # query "copies_available greater than 0".
    available = django_filters.BooleanFilter(method='filter_available')

    class Meta:
        model = Book
        # ?author=<id> becomes an automatic exact-match filter.
        fields = ['author']

    def filter_available(self, queryset, name, value):
        if value is True:
            return queryset.filter(copies_available__gt=0)   # only available
        if value is False:
            return queryset.filter(copies_available=0)        # only unavailable
        return queryset

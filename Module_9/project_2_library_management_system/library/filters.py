# ============================================================================
#  filters.py — ?author=&available=true catalog filters.
# ============================================================================
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    # ?available=true -> only books with at least one free copy.
    available = django_filters.BooleanFilter(method="filter_available")

    def filter_available(self, qs, name, value):
        if value:
            return qs.filter(copies_available__gt=0)
        return qs.filter(copies_available=0)

    class Meta:
        model = Book
        fields = ["author"]

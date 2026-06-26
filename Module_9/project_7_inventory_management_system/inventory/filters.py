# ============================================================================
#  filters.py — ?category=&supplier=&low_stock=true product filters.
# ============================================================================
import django_filters
from django.db.models import F
from .models import Product


class ProductFilter(django_filters.FilterSet):
    # ?low_stock=true -> quantity at or below the reorder level (uses F()).
    low_stock = django_filters.BooleanFilter(method="filter_low_stock")

    def filter_low_stock(self, qs, name, value):
        if value:
            return qs.filter(quantity__lte=F("reorder_level"))
        return qs.filter(quantity__gt=F("reorder_level"))

    class Meta:
        model = Product
        fields = ["category", "supplier"]

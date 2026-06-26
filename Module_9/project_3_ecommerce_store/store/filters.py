# ============================================================================
#  filters.py — ?category=&min_price=&max_price=&in_stock=true catalog filters.
# ============================================================================
import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")

    def filter_in_stock(self, qs, name, value):
        return qs.filter(stock__gt=0) if value else qs

    class Meta:
        model = Product
        fields = ["category"]

# ============================================================================
#  filters.py — the ?query=parameters clients can filter products by
# ----------------------------------------------------------------------------
#  Works with DjangoFilterBackend (switched on in api_views.py). Examples:
#     /api/products/?category=2           -> only products in category #2
#     /api/products/?min_price=100        -> price >= 100
#     /api/products/?max_price=500        -> price <= 500
#     /api/products/?min_price=100&max_price=500  -> price between 100 and 500
# ============================================================================
import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    # ?min_price=100 means "price Greater Than or Equal to 100".
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    # ?max_price=500 means "price Less Than or Equal to 500".
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category']   # ?category=<id> exact-match filter

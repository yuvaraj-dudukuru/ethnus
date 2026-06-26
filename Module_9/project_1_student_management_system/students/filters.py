# ============================================================================
#  filters.py — ?department=&is_active=&min_marks=&max_marks= query filters.
# ============================================================================
import django_filters
from .models import Student


class StudentFilter(django_filters.FilterSet):
    min_marks = django_filters.NumberFilter(field_name="marks", lookup_expr="gte")
    max_marks = django_filters.NumberFilter(field_name="marks", lookup_expr="lte")

    class Meta:
        model = Student
        fields = ["department", "is_active"]

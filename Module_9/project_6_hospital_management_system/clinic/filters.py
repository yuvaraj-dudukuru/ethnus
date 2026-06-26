# ============================================================================
#  filters.py — ?department=&specialization= doctor search filters.
# ============================================================================
import django_filters
from .models import Doctor


class DoctorFilter(django_filters.FilterSet):
    specialization = django_filters.CharFilter(
        field_name="specialization", lookup_expr="icontains")

    class Meta:
        model = Doctor
        fields = ["department", "specialization"]

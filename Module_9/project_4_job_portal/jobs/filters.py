# ============================================================================
#  filters.py — ?location=&type= job search filters.
# ============================================================================
import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(field_name="location", lookup_expr="icontains")

    class Meta:
        model = Job
        fields = ["type", "location"]

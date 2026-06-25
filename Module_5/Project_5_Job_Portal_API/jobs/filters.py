# ============================================================================
#  filters.py — the ?query=parameters clients can filter jobs by
# ----------------------------------------------------------------------------
#  Works with DjangoFilterBackend (switched on in api_views.py). Examples:
#     /api/jobs/?location=Delhi     -> jobs whose location contains "Delhi"
#     /api/jobs/?jtype=FT           -> only Full Time jobs
#     /api/jobs/?search=python      -> (SearchFilter) title/description match
# ============================================================================
import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    # Case-insensitive "contains" match, so ?location=del finds "Delhi".
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Job
        # ?jtype=FT / PT / CT / IN  -> exact match on the job type.
        fields = ['jtype']

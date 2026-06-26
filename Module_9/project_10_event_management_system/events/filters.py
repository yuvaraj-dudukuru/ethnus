# ============================================================================
#  filters.py — ?venue=&upcoming=true&after=&before= event filters.
# ============================================================================
import django_filters
from django.utils import timezone
from .models import Event


class EventFilter(django_filters.FilterSet):
    upcoming = django_filters.BooleanFilter(method="filter_upcoming")
    after = django_filters.IsoDateTimeFilter(field_name="datetime", lookup_expr="gte")
    before = django_filters.IsoDateTimeFilter(field_name="datetime", lookup_expr="lte")

    def filter_upcoming(self, qs, name, value):
        now = timezone.now()
        return qs.filter(datetime__gte=now) if value else qs.filter(datetime__lt=now)

    class Meta:
        model = Event
        fields = ["venue"]

# ============================================================================
#  filters.py — defines the ?query=parameters clients can filter students by
# ----------------------------------------------------------------------------
#  This works together with DjangoFilterBackend (switched on in api_views.py).
#  It lets a client narrow down the student list using the URL, for example:
#
#     /api/students/?department=2          -> only students in department #2
#     /api/students/?is_active=true        -> only active students
#     /api/students/?min_marks=80          -> students with marks >= 80
#     /api/students/?min_marks=40&max_marks=60  -> marks between 40 and 60
# ============================================================================
import django_filters
from .models import Student


class StudentFilter(django_filters.FilterSet):
    # A custom filter: ?min_marks=80 means "marks Greater Than or Equal to 80".
    # field_name is the model column; lookup_expr='gte' is the comparison.
    min_marks = django_filters.NumberFilter(field_name='marks', lookup_expr='gte')

    # ?max_marks=60 means "marks Less Than or Equal to 60".
    max_marks = django_filters.NumberFilter(field_name='marks', lookup_expr='lte')

    class Meta:
        model = Student
        # These fields get simple exact-match filters automatically:
        #   ?department=<id>   and   ?is_active=<true/false>
        fields = ['department', 'is_active']

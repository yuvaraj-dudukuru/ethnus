# ============================================================================
#  api_views.py — the API's "brains": what happens on each request
# ----------------------------------------------------------------------------
#  A ViewSet bundles together all the standard actions for a resource:
#     list, create, retrieve, update, partial_update, destroy.
#  Combined with the router in campushub/urls.py, this one class produces the
#  whole family of /api/students/ endpoints — we barely write any code.
# ============================================================================
from datetime import date

from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Department, Student
from .serializers import DepartmentSerializer, StudentSerializer
from .filters import StudentFilter

# The mark a student needs to "pass". Used by the pass/fail doughnut chart.
PASS_MARK = 40


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Departments are READ-ONLY through the API.

    ReadOnlyModelViewSet only provides list + retrieve (GET). There is no way
    to create/edit/delete a department via the API — that is done in the admin.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]   # anyone may read the department list


class StudentViewSet(viewsets.ModelViewSet):
    """Full CRUD for students (list, create, retrieve, update, delete)."""

    # select_related('department') fetches each student's department in the
    # SAME database query. Without it, listing 10 students would fire 10 extra
    # queries (the classic "N+1 problem"). This one word kills that problem.
    queryset = Student.objects.select_related('department')
    serializer_class = StudentSerializer

    # Default permission: read for everyone, write only for logged-in users.
    permission_classes = [IsAuthenticatedOrReadOnly]

    # The three backends that power filtering, searching and ordering.
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Use our StudentFilter class for ?department=&min_marks= etc.
    filterset_class = StudentFilter

    # ?search=ali looks for "ali" inside any of these fields (case-insensitive).
    search_fields = ['name', 'email', 'department__name']

    # ?ordering=marks (ascending) or ?ordering=-marks (descending) is allowed
    # only for these safe fields.
    ordering_fields = ['marks', 'roll', 'admitted']

    # If the client doesn't ask for an order, sort by highest marks first.
    ordering = ['-marks']

    def get_permissions(self):
        """Per-action permission tweak: only an ADMIN may DELETE a student.

        'destroy' is DRF's name for the DELETE action. For every other action
        we fall back to the default permission_classes above.
        """
        if self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def toppers(self, request):
        """Custom endpoint: GET /api/students/toppers/

        @action adds an EXTRA url beyond the standard CRUD set.
          - detail=False -> it acts on the whole list (/students/toppers/),
            not a single student (/students/5/toppers/).
        Returns the top 5 active students. Because the model is ordered by
        '-marks', "first 5 active students" = the 5 highest scorers.
        """
        qs = self.get_queryset().filter(is_active=True)[:5]
        return Response(self.get_serializer(qs, many=True).data)


class LogoutAPI(APIView):
    """POST /api/logout/ — log the current user out.

    Token authentication has no server "session" to end, so logging out means
    DELETING the user's token. After this, that token stops working and the
    user must log in again to get a new one. Only a logged-in user can do this.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # request.auth is the AuthToken object used for this request.
        # Deleting it invalidates the token immediately.
        if request.auth is not None:
            request.auth.delete()
        # 204 = "Success, and there is no content to send back."
        return Response(status=204)


class StatsView(APIView):
    """GET /api/stats/ — ALL the analytics numbers in ONE response.  (NEW in M6)

    This single endpoint powers the whole Analytics Dashboard:
      - the stat cards (total, average, top scorer, active count),
      - the BAR chart  (students per department),
      - the LINE chart (admissions per month),
      - the DOUGHNUT chart (pass vs fail).

    It is built entirely with the Django ORM's annotate()/aggregate() — i.e. the
    database does the counting and averaging, which is far faster than pulling
    every row into Python. Returning everything in one call means the front-end
    can refresh the entire dashboard with a single fetch.

    Optional date range:  ?start=YYYY-MM-DD&end=YYYY-MM-DD
    filters by each student's admission date, so the dashboard's date-range
    picker simply re-calls this endpoint with new dates.

    It is public (AllowAny) so the dashboard shows charts without a login. On a
    real site you would usually restrict analytics to staff (IsAdminUser).
    """
    permission_classes = [AllowAny]

    def _parse(self, value):
        """Safely turn a 'YYYY-MM-DD' string into a date, or None if invalid."""
        try:
            return date.fromisoformat(value) if value else None
        except (ValueError, TypeError):
            return None

    def get(self, request):
        # Start from all students, then narrow by the optional date range.
        qs = Student.objects.all()
        start = self._parse(request.query_params.get('start'))
        end = self._parse(request.query_params.get('end'))
        if start:
            qs = qs.filter(admitted__gte=start)
        if end:
            qs = qs.filter(admitted__lte=end)

        # --- Stat cards -----------------------------------------------------
        total = qs.count()
        # aggregate() returns a dict like {'marks__avg': 72.5}; default to 0.
        average = round(qs.aggregate(Avg('marks'))['marks__avg'] or 0, 1)
        active = qs.filter(is_active=True).count()
        top = qs.order_by('-marks').first()   # highest mark (model orders by -marks too)
        top_scorer = {'name': top.name, 'marks': top.marks} if top else None

        # --- BAR: students per department ----------------------------------
        # values() groups by department name; annotate(Count) counts each group.
        by_department = list(
            qs.values('department__name')
              .annotate(count=Count('id'))
              .order_by('-count')
        )
        by_department = [
            {'label': row['department__name'] or 'No department', 'count': row['count']}
            for row in by_department
        ]

        # --- LINE: admissions per month ------------------------------------
        # TruncMonth chops each admission date down to the first of its month,
        # so all students admitted in the same month group together.
        by_month = list(
            qs.annotate(month=TruncMonth('admitted'))
              .values('month')
              .annotate(count=Count('id'))
              .order_by('month')
        )
        admissions_by_month = [
            {'label': row['month'].strftime('%b %Y') if row['month'] else '—',
             'count': row['count']}
            for row in by_month
        ]

        # --- DOUGHNUT: pass vs fail ----------------------------------------
        passed = qs.filter(marks__gte=PASS_MARK).count()
        failed = total - passed

        return Response({
            'cards': {
                'total': total,
                'average': average,
                'active': active,
                'top_scorer': top_scorer,
            },
            'by_department': by_department,
            'admissions_by_month': admissions_by_month,
            'pass_fail': {'pass': passed, 'fail': failed, 'pass_mark': PASS_MARK},
        })

# ============================================================================
#  api_views.py — the API's "brains": what happens on each request
# ----------------------------------------------------------------------------
#  A ViewSet bundles together all the standard actions for a resource:
#     list, create, retrieve, update, partial_update, destroy.
#  Combined with the router in campushub/urls.py, this one class produces the
#  whole family of /api/students/ endpoints — we barely write any code.
# ============================================================================
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

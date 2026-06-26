# ============================================================================
#  api_views.py — the Student/Department API endpoints.
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from courses.models import Course
from .filters import StudentFilter
from .models import Department, Student, Enrollment
from .serializers import DepartmentSerializer, StudentSerializer, EnrollmentSerializer


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Departments are read-only via the API (managed in the admin)."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class StudentViewSet(viewsets.ModelViewSet):
    """Full CRUD for students + custom 'toppers' and 'enroll' actions."""

    queryset = (Student.objects
                .select_related("department")
                .prefetch_related("enrollments__course"))
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = StudentFilter
    search_fields = ["name", "email", "department__name"]
    ordering_fields = ["marks", "roll", "admitted"]
    ordering = ["-marks"]

    def get_permissions(self):
        # Only an admin may DELETE a student record.
        if self.action == "destroy":
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def toppers(self, request):
        """GET /api/students/toppers/ — the 5 highest-scoring active students."""
        qs = self.get_queryset().filter(is_active=True)[:5]
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        """POST /api/students/<id>/enroll/  body: {"course_id": 3}."""
        student = self.get_object()
        course = Course.objects.filter(pk=request.data.get("course_id")).first()
        if course is None:
            return Response({"detail": "course_id is invalid."}, status=400)
        enrollment, created = Enrollment.objects.get_or_create(
            student=student, course=course,
        )
        if not created:
            return Response({"detail": "Already enrolled in this course."}, status=400)
        return Response(EnrollmentSerializer(enrollment).data, status=201)

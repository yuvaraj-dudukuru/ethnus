# ============================================================================
#  api_views.py — catalog, enroll, mark-lesson-complete and progress %.
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Course, Lesson, Enrollment, Progress
from .permissions import IsInstructorOwnerOrReadOnly
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer


def progress_for(user, course):
    """Return {completed, total, percent} for a user on a course."""
    total = course.lessons.count()
    done = Progress.objects.filter(
        student=user, completed=True, lesson__course=course).count()
    percent = round(done / total * 100) if total else 0
    return {"completed": done, "total": total, "percent": percent}


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("instructor")
    serializer_class = CourseSerializer
    permission_classes = [IsInstructorOwnerOrReadOnly]
    search_fields = ["title", "description", "instructor__username"]
    filterset_fields = ["instructor"]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        """POST /api/courses/<id>/enroll/ — enrol the current student."""
        course = self.get_object()
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user, course=course)
        if not created:
            return Response({"detail": "Already enrolled."}, status=400)
        return Response(EnrollmentSerializer(enrollment).data, status=201)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def progress(self, request, pk=None):
        """GET /api/courses/<id>/progress/ — current student's completion %."""
        return Response(progress_for(request.user, self.get_object()))


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related("course")
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOwnerOrReadOnly]
    filterset_fields = ["course"]
    ordering = ["order"]

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        if course.instructor_id != self.request.user.id and not self.request.user.is_staff:
            raise PermissionDenied("You can only add lessons to your own course.")
        serializer.save()

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        """POST /api/lessons/<id>/complete/ — mark this lesson done."""
        lesson = self.get_object()
        Progress.objects.update_or_create(
            student=request.user, lesson=lesson, defaults={"completed": True})
        return Response(progress_for(request.user, lesson.course))


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """A student's own enrollments."""
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.select_related("course").filter(
            student=self.request.user)

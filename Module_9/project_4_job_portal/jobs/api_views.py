# ============================================================================
#  api_views.py — job board with role-based access + resume upload on apply.
# ----------------------------------------------------------------------------
#  Role rules:
#    * Anyone           -> browse/search jobs.
#    * Recruiters       -> post jobs (own only to edit), see their applicants.
#    * Candidates       -> apply (multipart resume upload), see their own apps.
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from accounts.models import role_of
from accounts.permissions import (
    IsCandidate, IsRecruiter, IsRecruiterOwnerOrReadOnly,
)
from .filters import JobFilter
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.select_related("recruiter")
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOwnerOrReadOnly]
    filterset_class = JobFilter
    search_fields = ["title", "company", "description", "location"]
    ordering_fields = ["posted", "salary"]

    def perform_create(self, serializer):
        # The poster is always the logged-in recruiter (never trust the body).
        serializer.save(recruiter=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsCandidate],
            parser_classes=[MultiPartParser, FormParser])
    def apply(self, request, pk=None):
        """POST /api/jobs/<id>/apply/ (multipart) — fields: resume, cover_note."""
        job = self.get_object()
        if Application.objects.filter(job=job, candidate=request.user).exists():
            return Response({"detail": "You already applied to this job."}, status=400)
        resume = request.FILES.get("resume")
        if not resume:
            return Response({"detail": "A resume file is required."}, status=400)
        app = Application.objects.create(
            job=job, candidate=request.user, resume=resume,
            cover_note=request.data.get("cover_note", ""))
        return Response(ApplicationSerializer(app).data, status=201)

    @action(detail=True, methods=["get"], permission_classes=[IsRecruiter])
    def applicants(self, request, pk=None):
        """GET /api/jobs/<id>/applicants/ — only the job's OWNER recruiter."""
        job = self.get_object()
        if job.recruiter_id != request.user.id:
            return Response({"detail": "Not your job posting."}, status=403)
        qs = job.applications.select_related("candidate")
        return Response(ApplicationSerializer(qs, many=True).data)


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """Role-shaped list: recruiters see applicants to THEIR jobs; candidates see
    only THEIR OWN applications."""
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        from rest_framework.permissions import IsAuthenticated
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = Application.objects.select_related("job", "candidate")
        user = self.request.user
        if role_of(user) == "recruiter":
            return qs.filter(job__recruiter=user)
        return qs.filter(candidate=user)

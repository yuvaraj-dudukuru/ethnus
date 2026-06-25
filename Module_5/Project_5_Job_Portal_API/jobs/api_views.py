# ============================================================================
#  api_views.py — the API's "brains": what happens on each request
# ----------------------------------------------------------------------------
#  This file shows the four new "muscles" of Project 5:
#    1) ROLE-BASED permission classes used end-to-end.
#    2) FILE UPLOAD through the API (the 'apply' action accepts multipart).
#    3) PER-ROLE querysets (recruiters and candidates see different data).
#    4) A STATUS-TRANSITION action (recruiter selects/rejects an applicant).
# ============================================================================
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend

from .models import Job, Application
from .serializers import (
    RegisterSerializer, JobSerializer, ApplicationSerializer,
)
from .filters import JobFilter
from .permissions import IsCandidate, IsRecruiterOwnerOrReadOnly


class RegisterAPI(APIView):
    """POST /api/register/ — create an account and pick a role.

    Body: {"username": ..., "password": ..., "role": "R" or "C"}
    Returns a ready-to-use auth token so the new user can start immediately.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'username': user.username, 'role': user.profile.role},
            status=status.HTTP_201_CREATED,
        )


class JobViewSet(viewsets.ModelViewSet):
    """Jobs: public to read, recruiter-only to post, owner-only to edit."""
    queryset = Job.objects.select_related('recruiter')
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description']   # ?search=python
    ordering_fields = ['created', 'title']

    def perform_create(self, serializer):
        # Stamp the logged-in recruiter as the job's owner.
        serializer.save(recruiter=self.request.user)

    @action(detail=True, methods=['post'],
            permission_classes=[IsCandidate],
            throttle_classes=[ScopedRateThrottle],
            parser_classes=[MultiPartParser, FormParser])   # accept file uploads
    def apply(self, request, pk=None):
        """POST /api/jobs/{id}/apply/ — a candidate applies, uploading a resume.

        This is sent as MULTIPART form-data (NOT raw JSON), because it carries
        a file. In Postman: Body -> form-data -> key 'resume' of type File,
        plus a text field 'cover_note'.

        The 'apply' scoped throttle limits each candidate to 10 applications
        per day (anti-spam).
        """
        job = self.get_object()
        ser = ApplicationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            # Stamp the job (from the URL) and the candidate (from the login).
            ser.save(candidate=request.user, job=job)
        except IntegrityError:
            # The unique_together (job, candidate) rule fired: already applied.
            return Response({'detail': 'Already applied.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ser.data, status=status.HTTP_201_CREATED)

    # The 'apply' action needs the scoped rate name attached to the view.
    throttle_scope = 'apply'


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """View applications — but WHICH ones you see depends on your role.

    This is the role-shaped queryset pattern: the SAME endpoint returns
    different data to different users, and nobody can see anyone else's data.
    """
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):                       # ⭐ ROLE-SHAPED data
        u = self.request.user
        if hasattr(u, 'profile') and u.profile.role == 'R':
            # A recruiter sees applications made to THEIR OWN jobs.
            return Application.objects.filter(job__recruiter=u).select_related('job', 'candidate')
        # A candidate sees only THEIR OWN applications.
        return Application.objects.filter(candidate=u).select_related('job', 'candidate')

    @action(detail=True, methods=['patch'])
    def set_status(self, request, pk=None):
        """PATCH /api/applications/{id}/set_status/  {"status": "S" or "R"}

        Only the recruiter who OWNS the job may select (S) or reject (R) an
        applicant. get_object() already limits this to the recruiter's own
        applications (via the role-shaped queryset), and we double-check
        ownership for safety.
        """
        application = self.get_object()

        # Must be a recruiter who owns the job this application is for.
        if not (hasattr(request.user, 'profile') and request.user.profile.role == 'R'
                and application.job.recruiter == request.user):
            return Response({'detail': 'Not allowed.'},
                            status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if new_status not in ('S', 'R'):
            return Response({'detail': "status must be 'S' (selected) or 'R' (rejected)."},
                            status=status.HTTP_400_BAD_REQUEST)

        application.status = new_status
        application.save(update_fields=['status'])
        return Response(ApplicationSerializer(application).data)


class LogoutAPI(APIView):
    """POST /api/logout/ — log the current user out by deleting their token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth is not None:
            request.auth.delete()
        return Response(status=204)   # 204 = success, nothing to send back

# ============================================================================
#  api_views.py — catalog browsing + issue/return + overdue report.
# ----------------------------------------------------------------------------
#  The headline lesson: the issue/return actions update copies_available with
#  an ATOMIC F() expression and a conditional filter, so two people borrowing
#  the last copy at the same moment can never push the count below zero.
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from django.db.models import F
from django.utils import timezone

from .filters import BookFilter
from .models import Author, Book, Member, Issue
from .serializers import (
    AuthorSerializer, BookSerializer, MemberSerializer, IssueSerializer,
)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    """Browse the catalog (public). Librarians (staff) manage books.
    Logged-in members issue/return copies."""
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = BookFilter
    search_fields = ["title", "isbn", "author__name"]
    ordering_fields = ["title", "copies_available"]

    def get_permissions(self):
        # Only librarians (staff) may create/edit/delete catalogue entries.
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return super().get_permissions()

    def _member_for(self, request):
        member, _ = Member.objects.get_or_create(
            user=request.user, defaults={"name": request.user.username})
        return member

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def issue(self, request, pk=None):
        """POST /api/books/<id>/issue/ — borrow a copy for the current member."""
        book = self.get_object()
        member = self._member_for(request)
        if Issue.objects.filter(book=book, member=member, returned=False).exists():
            return Response({"detail": "You already hold this book."}, status=400)
        # Atomic, race-safe stock decrement. Returns rows changed (0 = no stock).
        changed = (Book.objects
                   .filter(pk=book.pk, copies_available__gt=0)
                   .update(copies_available=F("copies_available") - 1))
        if not changed:
            return Response({"detail": "No copies available."}, status=400)
        issue = Issue.objects.create(
            book=book, member=member, due_date=Issue.default_due())
        return Response(IssueSerializer(issue).data, status=201)

    @action(detail=True, methods=["post"], url_path="return",
            permission_classes=[IsAuthenticated])
    def return_book(self, request, pk=None):
        """POST /api/books/<id>/return/ — return the current member's copy."""
        book = self.get_object()
        member = Member.objects.filter(user=request.user).first()
        issue = (Issue.objects.filter(book=book, member=member, returned=False).first()
                 if member else None)
        if issue is None:
            return Response({"detail": "No open loan for this book."}, status=400)
        today = timezone.now().date()
        issue.returned = True
        issue.return_date = today
        issue.fine = issue.compute_fine(today)
        issue.save()
        Book.objects.filter(pk=book.pk).update(
            copies_available=F("copies_available") + 1)
        return Response(IssueSerializer(issue).data)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]


class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    """Members see their own loans; librarians see everyone's."""
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Issue.objects.select_related("book", "member")
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            qs = qs.filter(member__user=user)
        return qs

    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def overdue(self, request):
        """GET /api/issues/overdue/ — librarian report of late, unreturned books."""
        today = timezone.now().date()
        qs = (Issue.objects.select_related("book", "member")
              .filter(returned=False, due_date__lt=today))
        return Response(self.get_serializer(qs, many=True).data)

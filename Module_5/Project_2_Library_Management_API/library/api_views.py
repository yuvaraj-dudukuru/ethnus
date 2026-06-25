# ============================================================================
#  api_views.py — the API's "brains": what happens on each request
# ----------------------------------------------------------------------------
#  This file shows the three new "muscles" of Project 2:
#    1) Custom business ACTIONS  -> issue a book, return a book.
#    2) A stock check + F() expression to safely change copies_available.
#    3) A computed REPORT endpoint (overdue books with fines).
# ============================================================================
from datetime import date

from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    DjangoModelPermissionsOrAnonReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Member, Issue
from .serializers import (
    BookSerializer, MemberSerializer, IssueSerializer,
)
from .filters import BookFilter


class BookViewSet(viewsets.ModelViewSet):
    """Full CRUD for books, plus the custom 'issue' action.

    Permission: DjangoModelPermissionsOrAnonReadOnly means:
      - ANYONE may READ books (GET), even when not logged in.
      - To WRITE (create/edit/delete) you must be logged in AND have the
        matching model permission (e.g. 'library.add_book'). Our seeded
        "Librarians" group has all those permissions, so librarians can write.
    """
    queryset = Book.objects.select_related('author')   # avoid N+1 queries
    serializer_class = BookSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'isbn']        # ?search=python looks in title + isbn
    ordering_fields = ['title', 'copies_available']

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def issue(self, request, pk=None):
        """POST /api/books/{id}/issue/  — lend this book to a member.

        Steps:
          1) Refuse if no copies are available (the stock check).
          2) Validate the incoming member + due_date with IssueSerializer.
          3) Save the new Issue, attaching THIS book.
          4) Decrease copies_available by 1 using F() — F does the subtraction
             inside the database itself, which is safe even if two people
             borrow at the exact same moment.
        """
        book = self.get_object()
        if not book.is_available:
            return Response({'detail': 'No copies available.'},
                            status=status.HTTP_400_BAD_REQUEST)
        ser = IssueSerializer(data=request.data)        # expects: member, due_date
        ser.is_valid(raise_exception=True)
        ser.save(book=book)
        book.copies_available = F('copies_available') - 1
        book.save(update_fields=['copies_available'])
        return Response(ser.data, status=status.HTTP_201_CREATED)


class MemberViewSet(viewsets.ModelViewSet):
    """Full CRUD for members — STAFF ONLY (member data is private)."""
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]   # only admin/staff users


class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    """Issues are READ-ONLY here (list + retrieve), staff only.

    New issues are NOT created directly on /api/issues/ — they are created by
    the books 'issue' action. The only write here is the 'return_book' action.
    """
    queryset = Issue.objects.select_related('book', 'member')
    serializer_class = IssueSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def return_book(self, request, pk=None):
        """POST /api/issues/{id}/return_book/ — accept a returned book.

        Marks the issue as returned, records today's date (this is what the
        fine @property uses), and puts the copy back on the shelf (+1 via F()).
        """
        issue = self.get_object()
        if issue.returned:
            return Response({'detail': 'This book was already returned.'},
                            status=status.HTTP_400_BAD_REQUEST)

        issue.returned = True
        issue.return_date = date.today()
        issue.save(update_fields=['returned', 'return_date'])

        # Put the physical copy back into stock.
        book = issue.book
        book.copies_available = F('copies_available') + 1
        book.save(update_fields=['copies_available'])

        # refresh_from_db() reloads the real number after the F() expression,
        # so the response shows the correct, up-to-date count.
        issue.refresh_from_db()
        return Response(IssueSerializer(issue).data, status=status.HTTP_200_OK)


class OverdueReport(APIView):
    """GET /api/reports/overdue/ — list every late, un-returned book.

    'Overdue' = not yet returned AND the due date is in the past. For each one
    we show the computed fine, and we add up a grand total at the end.
    Staff only.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = date.today()
        overdue = (Issue.objects
                   .filter(returned=False, due_date__lt=today)
                   .select_related('book', 'member'))
        data = IssueSerializer(overdue, many=True).data
        total_fine = sum(item['fine'] for item in data)   # add up all fines
        return Response({
            'count': overdue.count(),
            'total_fine': total_fine,
            'issues': data,
        })


class LogoutAPI(APIView):
    """POST /api/logout/ — log the current user out by deleting their token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth is not None:
            request.auth.delete()
        return Response(status=204)   # 204 = success, nothing to send back

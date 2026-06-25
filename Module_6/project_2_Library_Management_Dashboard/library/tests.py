# ============================================================================
#  tests.py — automated checks for the two trickiest pieces of logic
# ----------------------------------------------------------------------------
#  Run every test with:   python manage.py test
#
#  We test:
#    1) Trying to issue a book with ZERO copies left returns 400 (stock check).
#    2) The overdue report computes the right fine for a late, un-returned book.
#
#  Each test runs against a temporary throwaway database, so your real data is
#  never touched.
# ============================================================================
from datetime import date, timedelta

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from library.models import Author, Book, Member, Issue, FINE_PER_DAY


class LibraryAPITest(APITestCase):

    def setUp(self):
        # This runs before EACH test, giving every test a clean starting point.
        # An admin (staff) user — issuing/returning/reports require staff.
        self.admin = User.objects.create_superuser('admin', 'admin@a.com', 'admin')
        self.author = Author.objects.create(name='Test Author')
        self.member = Member.objects.create(name='Test Member', email='m@college.edu')

    def test_issue_beyond_stock_returns_400(self):
        # A book with NO copies available cannot be issued.
        book = Book.objects.create(
            title='Sold Out', isbn='0001', author=self.author,
            copies_total=1, copies_available=0,
        )
        # Log in as the admin for this request.
        self.client.force_authenticate(self.admin)
        due = (date.today() + timedelta(days=7)).isoformat()
        r = self.client.post(
            f'/api/books/{book.id}/issue/',
            {'member': self.member.id, 'due_date': due},
        )
        # 400 = "Bad Request" — our stock check rejected it.
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.data['detail'], 'No copies available.')

    def test_overdue_report_math(self):
        # A book issued 10 days ago, due 3 days ago, never returned => overdue.
        book = Book.objects.create(
            title='Late Book', isbn='0002', author=self.author,
            copies_total=2, copies_available=1,
        )
        issue = Issue.objects.create(
            book=book, member=self.member,
            due_date=date.today() - timedelta(days=3),   # 3 days overdue
            returned=False,
        )

        # The model @property should compute 3 days * FINE_PER_DAY.
        self.assertEqual(issue.fine, 3 * FINE_PER_DAY)

        # The report endpoint should include it and total the fines.
        self.client.force_authenticate(self.admin)
        r = self.client.get('/api/reports/overdue/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['count'], 1)
        self.assertEqual(r.data['total_fine'], 3 * FINE_PER_DAY)

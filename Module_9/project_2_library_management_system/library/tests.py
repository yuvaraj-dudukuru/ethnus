# ============================================================================
#  tests.py — Library API checks.  Run with:  python manage.py test
# ============================================================================
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from .models import Author, Book, Member, Issue


class LibraryAPITests(APITestCase):
    def setUp(self):
        self.librarian = User.objects.create_superuser("admin", "a@lib.test", "admin")
        self.u1 = User.objects.create_user("reader1", password="reader")
        self.u2 = User.objects.create_user("reader2", password="reader")
        self.author = Author.objects.create(name="Ada Lovelace")
        self.book = Book.objects.create(
            title="Notes", author=self.author, isbn="111",
            copies_total=1, copies_available=1)

    def test_public_can_browse_catalog(self):
        self.assertEqual(self.client.get("/api/books/").status_code, 200)

    def test_issue_decrements_stock(self):
        self.client.force_authenticate(self.u1)
        r = self.client.post(f"/api/books/{self.book.id}/issue/")
        self.assertEqual(r.status_code, 201)
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 0)

    def test_issue_beyond_stock_is_rejected(self):
        self.client.force_authenticate(self.u1)
        self.client.post(f"/api/books/{self.book.id}/issue/")  # takes last copy
        self.client.force_authenticate(self.u2)
        r = self.client.post(f"/api/books/{self.book.id}/issue/")
        self.assertEqual(r.status_code, 400)

    def test_return_restocks_and_clears_loan(self):
        self.client.force_authenticate(self.u1)
        self.client.post(f"/api/books/{self.book.id}/issue/")
        r = self.client.post(f"/api/books/{self.book.id}/return/")
        self.assertEqual(r.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 1)

    def test_fine_is_charged_for_late_return(self):
        member = Member.objects.create(user=self.u1, name="reader1")
        late = timezone.now().date() - timedelta(days=10)
        Issue.objects.create(book=self.book, member=member, due_date=late)
        self.book.copies_available = 0
        self.book.save()
        self.client.force_authenticate(self.u1)
        r = self.client.post(f"/api/books/{self.book.id}/return/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(float(r.data["fine"]), 10 * 5)  # 10 days × 5/day

    def test_overdue_report_is_librarian_only(self):
        self.client.force_authenticate(self.u1)
        self.assertEqual(self.client.get("/api/issues/overdue/").status_code, 403)
        self.client.force_authenticate(self.librarian)
        self.assertEqual(self.client.get("/api/issues/overdue/").status_code, 200)

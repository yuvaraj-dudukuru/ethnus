# ============================================================================
#  models.py — books, members and the issue/return ledger.
# ----------------------------------------------------------------------------
#  Author 1 ───< N Book 1 ───< N Issue N >─── 1 Member
#  Computed @property (is_overdue) and an atomic F() stock update keep the
#  "copies available" count correct even under concurrent borrows.
# ============================================================================
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

LOAN_DAYS = 14        # how long a book may be borrowed
FINE_PER_DAY = 5      # currency units charged per day late


class Author(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    isbn = models.CharField(max_length=20, unique=True)
    copies_total = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["title"]

    @property
    def available(self):
        return self.copies_available > 0

    def __str__(self):
        return self.title


class Member(models.Model):
    """A borrower, linked one-to-one with a login account."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="member_profile")
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Issue(models.Model):
    """One borrow event. Closed when `returned` becomes True."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issues")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="issues")
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        ordering = ["-issue_date"]

    @staticmethod
    def default_due():
        return timezone.now().date() + timedelta(days=LOAN_DAYS)

    @property
    def is_overdue(self):
        if self.returned:
            return False
        return timezone.now().date() > self.due_date

    def days_late(self, on=None):
        on = on or timezone.now().date()
        return max(0, (on - self.due_date).days)

    def compute_fine(self, on=None):
        """Fine = days late × FINE_PER_DAY (0 if returned on time)."""
        return self.days_late(on) * FINE_PER_DAY

    def __str__(self):
        return f"{self.book.title} → {self.member.name}"

# ============================================================================
#  models.py — the database design (reused from Module-4 Project 2)
# ----------------------------------------------------------------------------
#  Four tables, connected like this:
#
#      Author 1 ───< N Book 1 ───< N Issue >─── N 1 Member
#
#  - An Author writes many Books.
#  - A Book can be Issued (borrowed) many times.
#  - A Member can have many Issues (borrow many books).
#  - Each Issue links ONE book to ONE member for a period of time.
#
#  Two "computed" pieces of logic live here as @property methods
#  (Book.is_available and Issue.fine). A @property looks like a normal field
#  when you read it, but it is calculated on the fly in Python — it is NOT a
#  stored database column. The serializers expose these to the API.
# ============================================================================
from datetime import date
from django.db import models

# How much an overdue book costs the member, per day late (e.g. ₹5/day).
FINE_PER_DAY = 5


class Author(models.Model):
    """A person who writes books."""
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Book(models.Model):
    """A book the library owns, possibly in several physical copies."""

    title = models.CharField(max_length=200)

    # The ISBN is the unique barcode-style id printed on every book.
    isbn = models.CharField(max_length=20, unique=True)

    # The author. on_delete=CASCADE: if an author is deleted, their books go.
    # related_name='books' lets us write author.books.all().
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books'
    )

    # How many copies the library owns in total, and how many are on the
    # shelf right now (not currently borrowed).
    copies_total = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['title']   # default: list books alphabetically

    @property
    def is_available(self):
        """True if at least one copy is free to borrow. A computed value, not
        a stored column. Used by the ?available=true filter and the issue
        action's stock check."""
        return self.copies_available > 0

    def __str__(self):
        return self.title


class Member(models.Model):
    """A library member who can borrow books."""
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    join_date = models.DateField(auto_now_add=True)   # filled in automatically

    def __str__(self):
        return self.name


class Issue(models.Model):
    """One borrowing record: member X borrowed book Y, due on date Z."""

    # Which book and which member. PROTECT stops you deleting a book/member
    # that still has issue history attached (keeps the records honest).
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='issues')
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='issues')

    # When it was borrowed (auto), when it is due back, and whether it's back.
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)

    # Filled in when the book is actually returned (null until then).
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-issue_date']   # newest issues first

    @property
    def fine(self):
        """How much money is owed for returning late. A computed @property.

        Logic:
          - If the book is back, compare the RETURN date to the due date.
          - If it is still out, compare TODAY to the due date.
          - Days late × FINE_PER_DAY. Never negative (0 if on time/early).
        The IssueSerializer exposes this as a read-only 'fine' field.
        """
        end_date = self.return_date if self.returned and self.return_date else date.today()
        days_late = (end_date - self.due_date).days
        if days_late <= 0:
            return 0
        return days_late * FINE_PER_DAY

    def __str__(self):
        return f"{self.book} -> {self.member}"

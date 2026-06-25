# ============================================================================
#  serializers.py — translators between database objects and JSON
# ----------------------------------------------------------------------------
#  This project shows off "computed serializer fields": fields in the JSON
#  that are NOT plain database columns but are pulled from a related object
#  (book.title) or from a model @property (Issue.fine, Book.is_available).
# ============================================================================
from rest_framework import serializers
from .models import Author, Book, Member, Issue


class AuthorSerializer(serializers.ModelSerializer):
    """The shape of an Author in the API, plus a computed book count."""
    book_count = serializers.IntegerField(source='books.count', read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count']


class BookSerializer(serializers.ModelSerializer):
    """The shape of a Book in the API."""

    # COMPUTED, read-only field: the author's name pulled from the related
    # Author object (instead of just showing the author's id number).
    author_name = serializers.CharField(source='author.name', read_only=True)

    # COMPUTED, read-only field straight from the model @property is_available.
    # ReadOnlyField simply calls book.is_available and shows the result.
    is_available = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'author', 'author_name',
                  'copies_total', 'copies_available', 'is_available']
        # copies_available is changed only by the issue/return actions, never
        # directly through the book form — so we make it read-only here.
        read_only_fields = ['copies_available']


class MemberSerializer(serializers.ModelSerializer):
    """The shape of a Member in the API."""
    class Meta:
        model = Member
        fields = ['id', 'name', 'email', 'join_date']
        read_only_fields = ['join_date']   # set automatically on creation


class IssueSerializer(serializers.ModelSerializer):
    """The shape of an Issue (a borrowing record) — the signature serializer.

    It mixes real columns with three COMPUTED read-only fields:
      - book_title  : the title pulled from the related Book
      - member_name : the name pulled from the related Member
      - fine        : the model's @property, exposed via ReadOnlyField
    """

    book_title = serializers.CharField(source='book.title', read_only=True)
    member_name = serializers.CharField(source='member.name', read_only=True)
    fine = serializers.ReadOnlyField()                 # the model @property!

    class Meta:
        model = Issue
        fields = ['id', 'book', 'book_title', 'member', 'member_name',
                  'issue_date', 'due_date', 'returned', 'fine']
        # When borrowing a book, the URL already tells us WHICH book
        # (/api/books/{id}/issue/), so the client only sends member + due_date.
        # That is why 'book' is not required here — the issue action fills it
        # in with ser.save(book=book).
        extra_kwargs = {
            'book': {'required': False},
            'returned': {'required': False},
        }

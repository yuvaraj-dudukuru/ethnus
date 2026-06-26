# ============================================================================
#  serializers.py — JSON shapes for the library.
# ============================================================================
from rest_framework import serializers
from .models import Author, Book, Member, Issue


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(source="books.count", read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "book_count"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True)
    available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "author_id", "isbn",
                  "copies_total", "copies_available", "available"]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "name", "email"]


class IssueSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    member_name = serializers.CharField(source="member.name", read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Issue
        fields = ["id", "book", "book_title", "member", "member_name",
                  "issue_date", "due_date", "returned", "return_date",
                  "fine", "is_overdue"]
        read_only_fields = fields

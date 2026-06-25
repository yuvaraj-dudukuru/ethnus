# ============================================================================
#  admin.py — register our models with Django's built-in admin panel
# ----------------------------------------------------------------------------
#  This makes Authors, Books, Members and Issues editable at
#  http://127.0.0.1:8000/admin/ using a ready-made web interface.
# ============================================================================
from django.contrib import admin
from .models import Author, Book, Member, Issue


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'isbn', 'author', 'copies_available', 'copies_total']
    list_filter = ['author']
    search_fields = ['title', 'isbn']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'join_date']
    search_fields = ['name', 'email']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'member', 'issue_date', 'due_date', 'returned']
    list_filter = ['returned']

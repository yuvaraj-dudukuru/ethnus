from django.contrib import admin
from .models import Author, Book, Member, Issue


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "isbn", "copies_available", "copies_total"]
    list_filter = ["author"]
    search_fields = ["title", "isbn"]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "user"]
    search_fields = ["name", "email"]


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["book", "member", "issue_date", "due_date", "returned", "fine"]
    list_filter = ["returned"]

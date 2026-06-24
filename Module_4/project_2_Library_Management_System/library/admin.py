# Import the admin module from django to register our models to the Django Admin panel
from django.contrib import admin
# Import our models from the local directory
from .models import Author, Book, Member, Issue

# Use a decorator to register the Author model and its corresponding ModelAdmin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Specify which fields to display in the list view of the admin panel
    list_display = ('name',)

# Register the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Show these fields as columns in the admin list view, including computed property 'is_available'
    list_display = ('title', 'author', 'isbn', 'copies_total', 'copies_available', 'is_available')
    # Add a search bar that searches by title, isbn, or the related author's name
    search_fields = ('title', 'isbn', 'author__name')

# Register the Member model
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # Show name, email, and joined date
    list_display = ('name', 'email', 'joined')
    # Add search functionality for name and email
    search_fields = ('name', 'email')

# Register the Issue model
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    # Display the related book, member, dates, return status, and calculated fine
    list_display = ('book', 'member', 'issue_date', 'due_date', 'returned', 'fine')
    # Add a sidebar filter allowing filtering by the 'returned' boolean field
    list_filter = ('returned',)
    # Add a date drill-down navigation bar at the top of the list, using the issue_date
    date_hierarchy = 'issue_date'
    # Allow searching by related book's title or related member's name
    search_fields = ('book__title', 'member__name')

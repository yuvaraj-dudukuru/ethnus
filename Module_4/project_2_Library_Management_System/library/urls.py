# Import the path function to define URL patterns
from django.urls import path
# Import views from the current app directory
from . import views

# Define the application namespace so we can use 'library:book_list' in templates
app_name = 'library'

# Define the list of URL patterns that map URLs to specific views
urlpatterns = [
    # Map the root 'books/' URL to the BookListView
    path('books/', views.BookListView.as_view(), name='book_list'),
    # Map URLs like 'books/1/' to the BookDetailView, extracting '1' as the primary key (pk)
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    # Map the 'members/' URL to the MemberListView
    path('members/', views.MemberListView.as_view(), name='member_list'),
    # Map URLs like 'members/1/' to the MemberDetailView
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    # Map URLs like 'issue/1/' to the issue_book functional view, extracting '1' as book_id
    path('issue/<int:book_id>/', views.issue_book, name='issue_book'),
    # Map URLs like 'return/1/' to the return_book functional view, extracting '1' as issue_id
    path('return/<int:issue_id>/', views.return_book, name='return_book'),
    # Map the 'overdue/' URL to the OverdueReportView
    path('overdue/', views.OverdueReportView.as_view(), name='overdue_report'),
]

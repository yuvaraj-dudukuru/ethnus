# Import the path function to define URL patterns
from django.urls import path
# Import all the class-based views from the views.py file
from .views import (StudentListView, StudentDetailView, StudentCreateView,
                    StudentUpdateView, StudentDeleteView)

# Set the application namespace for URL reversing (e.g., 'students:index')
app_name = 'students'

# Define the list of URL patterns for the students app
urlpatterns = [
    # Map the root URL of this app to the StudentListView, named 'index'
    path('', StudentListView.as_view(), name='index'),
    # Map an integer primary key (pk) to the StudentDetailView, named 'detail'
    path('<int:pk>/', StudentDetailView.as_view(), name='detail'),
    # Map the 'add/' URL to the StudentCreateView, named 'add'
    path('add/', StudentCreateView.as_view(), name='add'),
    # Map the '<pk>/edit/' URL to the StudentUpdateView, named 'edit'
    path('<int:pk>/edit/', StudentUpdateView.as_view(), name='edit'),
    # Map the '<pk>/delete/' URL to the StudentDeleteView, named 'delete'
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='delete'),
]

# Import the path function used to route URLs to their corresponding views
from django.urls import path
# Import all the views from the current app's views module
from .views import (
    PostListView,
    PostDetailView,
    CategoryPostListView,
    PostCreateView,
    PostUpdateView,
    AuthorDashboardView,
    add_comment,
)

# Define the application namespace so we can cleanly reverse URLs using 'blog:name'
app_name = 'blog'

# A list containing all the URL patterns mapped to their respective views
urlpatterns = [
    # Map the root URL of this app to the PostListView to display all published posts
    path('', PostListView.as_view(), name='list'),
    
    # Map URLs with a category slug to the CategoryPostListView to filter posts by category
    # The <slug:slug> part captures a string and passes it as a keyword argument named 'slug'
    path('category/<slug:slug>/', CategoryPostListView.as_view(), name='category_list'),
    
    # Map the dashboard URL to AuthorDashboardView to show the logged-in user's posts
    path('dashboard/', AuthorDashboardView.as_view(), name='dashboard'),
    
    # Map the URL for creating a new post to the PostCreateView
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    
    # Map URLs with a post slug to the PostDetailView to show an individual post
    path('post/<slug:slug>/', PostDetailView.as_view(), name='detail'),
    
    # Map the edit URL for a specific post to the PostUpdateView
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_update'),
    
    # Map the comment submission URL for a specific post to the add_comment function view
    path('post/<slug:slug>/comment/', add_comment, name='add_comment'),
]

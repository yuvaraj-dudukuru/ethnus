# Import the path function for URL routing
from django.urls import path
# Import built-in Django authentication views and alias as auth_views
from django.contrib.auth import views as auth_views
# Import the custom register view from the current app
from .views import register

# Define the URL patterns for the accounts application
urlpatterns = [
    # Map the 'register/' URL to the custom register view function
    path('register/', register, name='register'),
    # Map the 'login/' URL to the built-in LoginView, explicitly setting the template path
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # Map the 'logout/' URL to the built-in LogoutView
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

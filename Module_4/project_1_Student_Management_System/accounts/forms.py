# Import the forms module from django
from django import forms
# Import the default built-in User model from django's auth system
from django.contrib.auth.models import User
# Import the built-in UserCreationForm which handles user registration automatically
from django.contrib.auth.forms import UserCreationForm

# Define a custom RegisterForm that inherits from UserCreationForm
class RegisterForm(UserCreationForm):
    # Inner Meta class to specify metadata for the form
    class Meta:
        # Link this form to the built-in User model
        model = User
        # Expose the username and email fields to the registration form
        fields = ['username', 'email']

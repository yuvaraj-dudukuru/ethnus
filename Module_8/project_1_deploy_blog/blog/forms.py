# Import Django's forms module to create form classes mapped to models
from django import forms
# Import the Comment and Post models to generate forms based on them
from .models import Comment, Post

# Define a ModelForm for the Comment model to handle comment creation
class CommentForm(forms.ModelForm):
    # The Meta class tells Django which model to use and which fields to display
    class Meta:
        # Link this form to the Comment model
        model = Comment
        # Only expose the 'body' field to the user; post and user are handled behind the scenes
        fields = ['body']

# Define a ModelForm for the Post model to handle post creation and updating
class PostForm(forms.ModelForm):
    # The Meta class defines the configuration for this ModelForm
    class Meta:
        # Link this form to the Post model
        model = Post
        # Expose these specific fields to the user via the form interface
        # Note: the 'author' field is deliberately excluded as it's set automatically in the view
        fields = ['title', 'slug', 'body', 'category', 'status']

# Import Django's admin module to register models with the backend interface
from django.contrib import admin
# Import our custom models: Category, Post, and Comment
from .models import Category, Post, Comment

# Register the Category model to make it accessible in the Django admin site
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Automatically populate the 'slug' field based on the text entered in the 'name' field
    prepopulated_fields = {'slug': ('name',)}

# Define an inline admin configuration for the Comment model
# TabularInline displays the related comments in a table format underneath the parent object (Post)
class CommentInline(admin.TabularInline):
    # Specify the model this inline will represent
    model = Comment
    # Set the number of empty extra forms to display to 0 (cleaner interface)
    extra = 0

# Register the Post model with customized list views and editing forms
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Define which columns are displayed in the list view of posts
    list_display = ('title', 'author', 'category', 'status', 'created')
    # Add a filtering sidebar to filter posts by their status or category
    list_filter = ('status', 'category')
    # Automatically populate the 'slug' field using the 'title' field's text
    prepopulated_fields = {'slug': ('title',)}
    # Include the CommentInline class to allow editing comments directly from the post's page
    inlines = [CommentInline]

# Register the Comment model independently to view all comments across the site
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Display the related post, the user who wrote it, and the creation time in the list view
    list_display = ('post', 'user', 'created')

# ============================================================================
#  admin.py — register our models with Django's built-in admin panel
# ----------------------------------------------------------------------------
#  Makes Categories, Posts and Comments editable at
#  http://127.0.0.1:8000/admin/ using a ready-made web interface.
# ============================================================================
from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'author', 'category', 'status', 'created']
    list_filter = ['status', 'category']
    search_fields = ['title', 'body']
    # Auto-fill the slug field in the admin form as you type the title.
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created']
    search_fields = ['body']

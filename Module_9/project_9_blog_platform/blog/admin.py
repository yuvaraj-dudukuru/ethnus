from django.contrib import admin
from .models import Category, Post, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "status", "category", "created"]
    list_filter = ["status", "category"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CommentInline]


admin.site.register(Comment)
admin.site.register(Like)

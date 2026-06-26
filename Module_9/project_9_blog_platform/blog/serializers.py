# ============================================================================
#  serializers.py — JSON shapes for the blog.
# ============================================================================
from rest_framework import serializers
from .models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "user", "body", "created"]
        read_only_fields = ["id", "user", "created"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category",
        write_only=True, required=False, allow_null=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "body", "status", "author", "category",
                  "category_id", "like_count", "comment_count", "liked_by_me",
                  "created"]
        read_only_fields = ["id", "slug", "author", "created"]

    def get_liked_by_me(self, obj):
        user = self.context["request"].user
        return user.is_authenticated and obj.likes.filter(user=user).exists()

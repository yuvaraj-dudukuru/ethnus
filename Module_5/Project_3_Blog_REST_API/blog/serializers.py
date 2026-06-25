# ============================================================================
#  serializers.py — translators between database objects and JSON
# ----------------------------------------------------------------------------
#  This project shows the "two-serializer pattern": a SLIM serializer for list
#  views (just enough to show a feed) and a RICH serializer for the detail
#  view (the full article with its body and comment count). Using a light
#  serializer for lists keeps big list responses fast and small.
# ============================================================================
from rest_framework import serializers
from .models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    """The shape of a Category, plus how many posts it has."""
    post_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'post_count']


class CommentSerializer(serializers.ModelSerializer):
    """The shape of a Comment."""

    # Show the commenter's username instead of just their id number.
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'user_name', 'body', 'created']
        # 'post' and 'user' are filled in by the server (from the URL slug and
        # the logged-in user), never sent by the client — so they're read-only.
        read_only_fields = ['post', 'user', 'created']


class PostListSerializer(serializers.ModelSerializer):
    """SLIM serializer used for the LIST view (the feed).

    It leaves out the heavy 'body' text so a page of 10 posts stays small.
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author_name',
                  'category_name', 'status', 'created']


class PostSerializer(serializers.ModelSerializer):
    """RICH serializer used for create / retrieve / update (the full article)."""

    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    # A computed count of how many comments this post has.
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'body', 'author', 'author_name',
                  'category', 'category_name', 'status',
                  'comment_count', 'created', 'updated']
        # The server controls these:
        #  - slug is auto-generated from the title
        #  - author is stamped from the logged-in user (perform_create)
        #  - created/updated are timestamps
        read_only_fields = ['slug', 'author', 'created', 'updated']

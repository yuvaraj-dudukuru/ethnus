# ============================================================================
#  api_views.py — the API's "brains": what happens on each request
# ----------------------------------------------------------------------------
#  This file shows the four new "muscles" of Project 3:
#    1) IsOwnerOrReadOnly      -> strangers can read your post but not edit it.
#    2) Slug lookups           -> /api/posts/django-tips/ instead of /posts/7/.
#    3) The two-serializer pattern -> slim list vs rich detail.
#    4) A nested comments route + a scoped anti-spam throttle.
# ============================================================================
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle

from .models import Category, Post
from .serializers import (
    CategorySerializer, PostSerializer, PostListSerializer, CommentSerializer,
)
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Full CRUD for posts — the heart of the blog API."""

    serializer_class = PostSerializer

    # Two permission classes work together:
    #  - IsAuthenticatedOrReadOnly: read for all, must log in to write.
    #  - IsOwnerOrReadOnly: of the logged-in writers, only the AUTHOR may
    #    edit/delete THIS post.
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # Look posts up by their slug, so the URL is /api/posts/django-tips/.
    lookup_field = 'slug'

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']     # ?search=django looks in title + body
    ordering = ['-created']               # newest first by default

    def get_queryset(self):
        """Hide drafts from the public list.

        On the LIST action we return only Published posts. For a single post
        (retrieve/update/delete) we return everything, and the permission +
        owner checks decide what each user is allowed to do.
        """
        qs = Post.objects.select_related('author', 'category')   # avoid N+1 queries
        if self.action == 'list':
            return qs.filter(status='P')
        return qs

    def get_serializer_class(self):
        """Use the SLIM serializer for the feed, the RICH one everywhere else."""
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        """Stamp the new post with the logged-in user as its author.

        The client never sends 'author' — we set it here from the request, so
        nobody can post in someone else's name.
        """
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Categories are READ-ONLY through the API (list + retrieve)."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostCommentsAPIView(generics.ListCreateAPIView):
    """The NESTED route:  /api/posts/{slug}/comments/

    GET  -> list the comments on that post (anyone may read).
    POST -> add a comment (must be logged in). The user and the post are
            stamped automatically, so the client only sends 'body'.

    Anti-spam: this view uses the SCOPED 'comments' throttle (30/hour),
    separate from the global limits.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comments'          # ties this view to the '30/hour' rate

    def get_post(self):
        """Fetch the post named in the URL slug (404 if it doesn't exist)."""
        return get_object_or_404(Post, slug=self.kwargs['slug'])

    def get_queryset(self):
        # Only the comments belonging to this particular post.
        return self.get_post().comments.select_related('user')

    def perform_create(self, serializer):
        # Stamp BOTH the post (from the URL) and the user (from the login).
        serializer.save(user=self.request.user, post=self.get_post())


class MyPostsView(generics.ListAPIView):
    """GET /api/my-posts/ — the logged-in user's OWN posts, drafts included."""
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]    # must be logged in

    def get_queryset(self):
        # request.user.posts is every post this user authored (any status).
        return self.request.user.posts.select_related('author', 'category')


class LogoutAPI(APIView):
    """POST /api/logout/ — log the current user out by deleting their token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth is not None:
            request.auth.delete()
        return Response(status=204)   # 204 = success, nothing to send back

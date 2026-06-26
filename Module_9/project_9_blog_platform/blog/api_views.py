# ============================================================================
#  api_views.py — posts (draft-aware), comments and a like toggle.
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .models import Category, Post, Comment, Like
from .permissions import IsAuthorOrReadOnly
from .serializers import CategorySerializer, PostSerializer, CommentSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = "slug"
    filterset_fields = ["category", "status"]
    search_fields = ["title", "body"]

    def get_queryset(self):
        qs = (Post.objects.select_related("author", "category")
              .prefetch_related("likes", "comments"))
        user = self.request.user
        if not user.is_authenticated:
            return qs.filter(status="PUBLISHED")
        if user.is_staff:
            return qs
        # Authors can see their OWN drafts plus everyone's published posts.
        return qs.filter(Q(status="PUBLISHED") | Q(author=user))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        """POST /api/posts/<slug>/like/ — toggle like (drives optimistic UI)."""
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        # Count via the model (not post.likes) to bypass the prefetch cache.
        count = Like.objects.filter(post=post).count()
        return Response({"liked": created, "like_count": count})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("user", "post")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filterset_fields = ["post"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

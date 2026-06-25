# ============================================================================
#  urls.py — the project's master "address book"
# ----------------------------------------------------------------------------
#  A DRF "router" builds all the standard CRUD URLs for each ViewSet. On top
#  of that we hand-write three special URLs:
#     - the NESTED comments route  /api/posts/{slug}/comments/
#     - the "my posts" route       /api/my-posts/
#     - login / logout / docs
# ============================================================================
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # serves a plain HTML page (NEW in M6)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from blog.api_views import (
    PostViewSet, CategoryViewSet, PostCommentsAPIView, MyPostsView,
    LogoutAPI, MeView,
)

# 1) Register the two ViewSets with the router.
router = DefaultRouter()
# PostViewSet defines get_queryset() (not a plain 'queryset' attribute), so the
# router can't guess a name for it — we supply one explicitly with basename.
router.register('posts', PostViewSet, basename='post')   # /api/posts/  and  /api/posts/{slug}/
router.register('categories', CategoryViewSet)   # /api/categories/

# 2) The full list of URL patterns.
urlpatterns = [
    # --- Module 6: the front-end dashboard page ---
    # The home page ("/") renders blog/templates/blog/dashboard.html. All the
    # live behaviour (cards, comments, likes) is done by JavaScript talking to
    # the API below.
    path('', TemplateView.as_view(template_name='blog/dashboard.html'),
         name='dashboard'),

    path('admin/', admin.site.urls),

    # "Who am I?" — the front-end auth check (NEW in M6).
    path('api/me/', MeView.as_view(), name='api-me'),

    # The "my posts" route (own posts including drafts). Defined BEFORE the
    # router so it is matched first.
    path('api/my-posts/', MyPostsView.as_view(), name='my-posts'),

    # The NESTED comments route. {slug} identifies which post the comments
    # belong to. Also defined before the router so it wins the match.
    path('api/posts/<slug:slug>/comments/',
         PostCommentsAPIView.as_view(), name='post-comments'),

    # All router-generated API URLs.
    path('api/', include(router.urls)),

    # --- Authentication endpoints ---
    path('api/login/', obtain_auth_token, name='api-login'),   # POST -> {"token": ...}
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),

    # --- Auto-generated documentation ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

# Handy URLs (also in the README):
#   http://127.0.0.1:8000/api/                          -> browsable API root
#   http://127.0.0.1:8000/api/posts/                    -> published posts
#   http://127.0.0.1:8000/api/posts/<slug>/             -> one post by slug
#   http://127.0.0.1:8000/api/posts/<slug>/comments/    -> that post's comments
#   http://127.0.0.1:8000/api/my-posts/                 -> your own posts (auth)
#   http://127.0.0.1:8000/api/docs/                     -> Swagger documentation
#   http://127.0.0.1:8000/admin/                        -> admin panel (admin / admin)

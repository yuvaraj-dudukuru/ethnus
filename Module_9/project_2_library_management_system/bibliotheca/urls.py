# ============================================================================
#  urls.py — frontend + API router + auth + Swagger + admin.
# ============================================================================
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from library.api_views import (
    AuthorViewSet, BookViewSet, MemberViewSet, IssueViewSet,
)

router = DefaultRouter()
router.register("authors", AuthorViewSet)
router.register("books", BookViewSet)
router.register("members", MemberViewSet)
router.register("issues", IssueViewSet, basename="issue")

urlpatterns = [
    path("", TemplateView.as_view(template_name="catalog.html"), name="home"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/login/", obtain_auth_token, name="api-login"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

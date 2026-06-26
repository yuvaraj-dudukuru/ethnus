# ============================================================================
#  urls.py — the project's master address book.
# ----------------------------------------------------------------------------
#  Frontend page  +  DRF router API  +  auth  +  Swagger docs  +  admin.
# ============================================================================
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from courses.api_views import CourseViewSet
from students.api_views import DepartmentViewSet, StudentViewSet

router = DefaultRouter()
router.register("departments", DepartmentViewSet)
router.register("students", StudentViewSet)
router.register("courses", CourseViewSet)

urlpatterns = [
    # Frontend (server-rendered shell; the JS calls the API).
    path("", TemplateView.as_view(template_name="dashboard.html"), name="home"),

    # Browser login/logout for the frontend (session auth).
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("admin/", admin.site.urls),

    # REST API.
    path("api/", include(router.urls)),
    path("api/login/", obtain_auth_token, name="api-login"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

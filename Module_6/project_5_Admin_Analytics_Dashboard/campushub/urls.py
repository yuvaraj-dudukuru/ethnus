# ============================================================================
#  urls.py — the project's master "address book"
# ----------------------------------------------------------------------------
#  Every URL the website answers is listed here. When a request comes in,
#  Django reads this file top-to-bottom to decide which view should handle it.
#
#  We use a DRF "router". A router is a shortcut: you register a ViewSet with
#  it once, and it automatically creates ALL the standard URLs for you:
#     /api/students/        (list + create)
#     /api/students/5/      (retrieve + update + delete one)
#     /api/students/toppers/ (our custom action)
#  ...and the same set for departments.
# ============================================================================
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # serves a plain HTML page (NEW in M6)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token  # ready-made login view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from students.api_views import (
    StudentViewSet, DepartmentViewSet, LogoutAPI, StatsView,
)

# 1) Create a router and register our two ViewSets with it.
router = DefaultRouter()
router.register('students', StudentViewSet)        # builds all /api/students/... URLs
router.register('departments', DepartmentViewSet)  # builds all /api/departments/... URLs

# 2) The full list of URL patterns for the project.
urlpatterns = [
    # --- Module 6: the front-end analytics dashboard page ---
    # The home page ("/") renders students/templates/students/dashboard.html.
    # All the charts are drawn by JavaScript from the /api/stats/ data below.
    path('', TemplateView.as_view(template_name='students/dashboard.html'),
         name='dashboard'),

    # The single aggregate endpoint that feeds the whole dashboard (NEW in M6).
    path('api/stats/', StatsView.as_view(), name='stats'),

    # The classic Django admin control panel (login with admin / admin).
    path('admin/', admin.site.urls),

    # All router-generated API URLs get the "api/" prefix.
    path('api/', include(router.urls)),

    # --- Authentication endpoints ---
    # POST username + password here and you get back {"token": "..."}.
    path('api/login/', obtain_auth_token, name='api-login'),
    # POST here (with your token) to log out — it deletes your token.
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),

    # --- Auto-generated documentation ---
    # The raw OpenAPI schema (machine-readable JSON/YAML).
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # The friendly, interactive Swagger UI docs page (open this in a browser).
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

# Helpful URLs to remember (also listed in the README):
#   http://127.0.0.1:8000/api/           -> browsable API root
#   http://127.0.0.1:8000/api/docs/      -> Swagger documentation
#   http://127.0.0.1:8000/admin/         -> admin panel (admin / admin)

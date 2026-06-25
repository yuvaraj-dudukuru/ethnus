# ============================================================================
#  urls.py — the project's master "address book"
# ----------------------------------------------------------------------------
#  A DRF "router" builds the standard URLs for the job and application
#  ViewSets (plus their @action routes: apply, set_status). We add a register
#  endpoint, login/logout, the docs, and — importantly — a rule to serve the
#  uploaded resume files while developing.
# ============================================================================
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from jobs.api_views import (
    JobViewSet, ApplicationViewSet, RegisterAPI, LogoutAPI,
)

# 1) Register the ViewSets with the router.
router = DefaultRouter()
router.register('jobs', JobViewSet)                          # /api/jobs/... (+ /jobs/{id}/apply/)
router.register('applications', ApplicationViewSet,          # /api/applications/...
                basename='application')                      # (+ /applications/{id}/set_status/)

# 2) The full list of URL patterns.
urlpatterns = [
    path('admin/', admin.site.urls),

    # Sign up: choose a role (Recruiter or Candidate) and get a token back.
    path('api/register/', RegisterAPI.as_view(), name='register'),

    # All router-generated API URLs (jobs, applications).
    path('api/', include(router.urls)),

    # --- Authentication endpoints ---
    path('api/login/', obtain_auth_token, name='api-login'),   # POST -> {"token": ...}
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),

    # --- Auto-generated documentation ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

# While DEBUG is on, let Django serve the uploaded resume files at /media/...
# (In production a real web server handles this instead.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handy URLs (also in the README):
#   http://127.0.0.1:8000/api/register/   -> sign up (choose role)
#   http://127.0.0.1:8000/api/jobs/       -> public job listings
#   http://127.0.0.1:8000/api/applications/ -> your applications (role-shaped)
#   http://127.0.0.1:8000/api/docs/       -> Swagger documentation
#   http://127.0.0.1:8000/admin/          -> admin panel (admin / admin)

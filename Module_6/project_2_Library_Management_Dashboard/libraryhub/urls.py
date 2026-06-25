# ============================================================================
#  urls.py — the project's master "address book"
# ----------------------------------------------------------------------------
#  A DRF "router" automatically builds all the standard CRUD URLs for each
#  ViewSet we register, plus the URLs for any @action methods (issue,
#  return_book). We then add a few extra hand-written URLs (login, logout,
#  the overdue report, and the docs).
# ============================================================================
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # serves a plain HTML page (NEW in M6)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from library.api_views import (
    AuthorViewSet, BookViewSet, MemberViewSet, IssueViewSet,
    OverdueReport, LogoutAPI,
)

# 1) Register the ViewSets with the router.
router = DefaultRouter()
router.register('books', BookViewSet)       # /api/books/...  (+ /books/{id}/issue/)
router.register('members', MemberViewSet)   # /api/members/...
router.register('issues', IssueViewSet)     # /api/issues/... (+ /issues/{id}/return_book/)
router.register('authors', AuthorViewSet)   # /api/authors/   (NEW in M6: filter dropdown)

# 2) The full list of URL patterns.
urlpatterns = [
    # --- Module 6: the front-end dashboard page ---
    # The home page ("/") renders library/templates/library/dashboard.html.
    # TemplateView just renders a template with no extra Python logic — all the
    # live behaviour (filtering books, issuing/returning) is done by JavaScript
    # talking to the API below.
    path('', TemplateView.as_view(template_name='library/dashboard.html'),
         name='dashboard'),

    # The classic Django admin control panel (login with admin / admin).
    path('admin/', admin.site.urls),

    # All router-generated API URLs get the "api/" prefix.
    path('api/', include(router.urls)),

    # The overdue-books report (staff only). Not part of a ViewSet, so it gets
    # its own URL.
    path('api/reports/overdue/', OverdueReport.as_view(), name='overdue-report'),

    # --- Authentication endpoints ---
    path('api/login/', obtain_auth_token, name='api-login'),   # POST -> {"token": ...}
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),

    # --- Auto-generated documentation ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

# Handy URLs (also in the README):
#   http://127.0.0.1:8000/api/                 -> browsable API root
#   http://127.0.0.1:8000/api/docs/            -> Swagger documentation
#   http://127.0.0.1:8000/api/reports/overdue/ -> overdue report (staff)
#   http://127.0.0.1:8000/admin/               -> admin panel (admin / admin)

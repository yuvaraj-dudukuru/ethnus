# Import the admin module to route admin URLs
from django.contrib import admin
# Import path for standard URL routing and include to reference app URLs
from django.urls import path, include
# Import settings to access MEDIA configuration in DEBUG mode
from django.conf import settings
# Import static to serve media files during development
from django.conf.urls.static import static

# Define the root URL patterns for the entire Django project
urlpatterns = [
    # Route 'admin/' to the built-in Django Admin interface
    path('admin/', admin.site.urls),
    # Route the empty path '' (homepage) to the students app URLs
    path('', include('students.urls')),
    # Route 'accounts/' to the accounts app URLs (for register, login, logout)
    path('accounts/', include('accounts.urls')),
]

# If the project is running in development mode (DEBUG=True)
if settings.DEBUG:
    # Append the static URL pattern to serve media files (like student photos)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

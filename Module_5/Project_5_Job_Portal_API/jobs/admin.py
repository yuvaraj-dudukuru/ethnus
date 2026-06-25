# ============================================================================
#  admin.py — register our models with Django's built-in admin panel
# ----------------------------------------------------------------------------
#  Makes Profiles, Jobs and Applications editable at
#  http://127.0.0.1:8000/admin/ (log in as admin / admin).
# ============================================================================
from django.contrib import admin
from .models import Profile, Job, Application


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role']
    list_filter = ['role']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'location', 'jtype', 'recruiter', 'created']
    list_filter = ['jtype']
    search_fields = ['title', 'description', 'location']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'candidate', 'status', 'applied_at']
    list_filter = ['status']

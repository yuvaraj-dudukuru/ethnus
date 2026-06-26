# ============================================================================
#  admin.py — register our models with Django's built-in admin panel
# ----------------------------------------------------------------------------
#  Doing this makes Department and Student show up at http://127.0.0.1:8000/admin/
#  where the admin user (admin / admin) can add, edit and delete records using
#  a ready-made web interface — no extra code needed.
# ============================================================================
from django.contrib import admin
from .models import Department, Student


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # Columns to show in the department list table.
    list_display = ['id', 'name']
    search_fields = ['name']        # adds a search box for the name


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Columns to show in the student list table.
    list_display = ['roll', 'name', 'email', 'marks', 'is_active', 'department']
    # Sidebar filters to quickly narrow the list.
    list_filter = ['is_active', 'department']
    # Search box that looks across these fields.
    search_fields = ['name', 'email', 'roll']

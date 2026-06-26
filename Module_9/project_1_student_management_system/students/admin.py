from django.contrib import admin
from .models import Department, Student, Enrollment


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["roll", "name", "email", "marks", "department", "is_active"]
    list_filter = ["department", "is_active"]
    search_fields = ["name", "email", "roll"]
    inlines = [EnrollmentInline]

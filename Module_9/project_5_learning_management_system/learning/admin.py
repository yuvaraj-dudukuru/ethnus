from django.contrib import admin
from .models import Course, Lesson, Enrollment, Progress


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "instructor", "lesson_count", "created"]
    search_fields = ["title"]
    inlines = [LessonInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "enrolled"]


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ["student", "lesson", "completed", "completed_at"]
    list_filter = ["completed"]

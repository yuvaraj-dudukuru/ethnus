# Django admin framework.
from django.contrib import admin
# The models we want to manage from the admin site.
from .models import Profile, Job, Application


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Columns shown in the Profiles list view.
    list_display = ('user', 'role', 'phone')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    # Columns shown in the Jobs list view.
    list_display = ('title', 'company', 'recruiter', 'location', 'jtype', 'active', 'posted')
    # Sidebar filters for quickly narrowing the list.
    list_filter = ('jtype', 'location', 'active')
    # Free-text search box across these fields.
    search_fields = ('title', 'company', 'location')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    # Columns shown in the Applications list view; 'resume_link' is the custom
    # method defined below (a clickable link instead of a raw file path).
    list_display = ('candidate', 'job', 'status', 'applied', 'resume_link')
    # Lets you change an application's status directly from the list page.
    list_editable = ('status',)
    # Filter applications by status, or by the job type they applied to.
    list_filter = ('status', 'job__jtype')

    def resume_link(self, obj):
        """Render the resume as a clickable 'View Resume' link in the admin."""
        # format_html safely builds HTML (escaping the URL) for the admin column.
        from django.utils.html import format_html
        # Only show a link if a resume file is actually attached.
        if obj.resume:
            return format_html('<a href="{}" target="_blank">View Resume</a>', obj.resume.url)
        return "No Resume"
    # The column header text for the method above.
    resume_link.short_description = 'Resume'

# Import the admin module to customize the Django admin interface
from django.contrib import admin
# Import the Department and Student models
from .models import Department, Student

# Define an inline admin class for Student to be used within DepartmentAdmin
class StudentInline(admin.TabularInline):
    # Specify the model to use for the inline
    model = Student
    # Set the number of extra empty forms to display to 1
    extra = 1

# Register the Department model with a custom ModelAdmin class using a decorator
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # Attach the StudentInline class so students can be managed directly on the Department page
    inlines = [StudentInline]

# Register the Student model with a custom ModelAdmin class using a decorator
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Specify which fields to display as columns in the list view
    list_display = ['roll', 'name', 'email', 'department', 'marks', 'is_active']
    # Enable a search box that searches by name, email, and roll number
    search_fields = ['name', 'email', 'roll']
    # Add a filter sidebar to filter students by department and active status
    list_filter = ['department', 'is_active']

# Import LoginRequiredMixin to restrict views to logged-in users only
from django.contrib.auth.mixins import LoginRequiredMixin
# Import Q objects to perform complex queries (like OR conditions)
from django.db.models import Q
# Import reverse_lazy to delay URL resolution until the view is accessed
from django.urls import reverse_lazy
# Import standard generic class-based views from Django
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
# Import the Student model from the current app
from .models import Student
# Import the custom StudentForm from the current app
from .forms import StudentForm

# Define a class-based view to list students
class StudentListView(ListView):
    # Specify the model to list
    model = Student; 
    # Specify the HTML template to render the list
    template_name = 'students/index.html'
    # Define the context variable name to be used in the template
    context_object_name = 'students'; 
    # Set pagination to display 10 students per page
    paginate_by = 10
    
    # Override the default queryset method to add custom logic
    def get_queryset(self):
        # Base query: Get all students and optimize database hits by fetching related departments
        qs = Student.objects.select_related('department')
        # Get the 'q' parameter from the URL query string (search term)
        q = self.request.GET.get('q', '')
        # If a search term was provided
        if q:
            # Filter the queryset where name contains 'q' OR email contains 'q' (case-insensitive)
            qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q))
        # Return the final filtered (or unfiltered) queryset
        return qs

# Define a class-based view to show details of a single student
class StudentDetailView(DetailView):
    # Specify the model to use
    model = Student; 
    # Specify the HTML template to render the details
    template_name = 'students/detail.html'; 
    # Define the context variable name to be used in the template
    context_object_name = 's'

# Define a class-based view to create a new student, requiring login
class StudentCreateView(LoginRequiredMixin, CreateView):
    # Specify the model to use
    model = Student; 
    # Specify the form class to handle user input
    form_class = StudentForm
    # Specify the HTML template for the form
    template_name = 'students/form.html'
    # Define the URL to redirect to upon successful creation
    success_url = reverse_lazy('students:index')

# Define a class-based view to update an existing student, requiring login
class StudentUpdateView(LoginRequiredMixin, UpdateView):
    # Specify the model to update
    model = Student; 
    # Specify the form class to handle user input
    form_class = StudentForm
    # Specify the HTML template for the form
    template_name = 'students/form.html'
    # Define the URL to redirect to upon successful update
    success_url = reverse_lazy('students:index')

# Define a class-based view to delete an existing student, requiring login
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    # Specify the model to delete
    model = Student; 
    # Specify the HTML template for the confirmation page
    template_name = 'students/confirm_delete.html'
    # Define the URL to redirect to upon successful deletion
    success_url = reverse_lazy('students:index')

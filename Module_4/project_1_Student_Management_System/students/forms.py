# Import the forms module from django to create forms
from django import forms
# Import the Student model from the current directory's models.py file
from .models import Student

# Define a StudentForm class that inherits from forms.ModelForm
class StudentForm(forms.ModelForm):
    # Inner Meta class to specify metadata for the form
    class Meta:
        # Link this form to the Student model
        model  = Student
        # Specify the exact fields to include in the form
        fields = ['roll', 'name', 'email', 'marks', 'department', 'photo']
        # Define custom widgets for specific fields using a dictionary comprehension
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'})
                   # Apply the TextInput widget with the 'form-control' CSS class to roll, name, email, and marks
                   for f in ['roll', 'name', 'email', 'marks']}
        # Override the widget for the department field to use a Select dropdown with 'form-select' CSS class
        widgets['department'] = forms.Select(attrs={'class': 'form-select'})
    
    # Define a custom validation method specifically for the 'email' field
    def clean_email(self):
        # Retrieve the email value that was submitted and initially cleaned by Django
        e = self.cleaned_data['email']
        # Check if the email does NOT end with the required domain '@college.edu'
        if not e.endswith('@college.edu'):
            # Raise a validation error if the domain condition is not met
            raise forms.ValidationError("Official @college.edu email required.")
        # Return the valid email to be saved in the database
        return e

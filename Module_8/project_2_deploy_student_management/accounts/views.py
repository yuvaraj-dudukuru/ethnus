# Import render to return HTML templates, and redirect to navigate to other URLs
from django.shortcuts import render, redirect
# Import messages to send flash messages (like success or error alerts) to the user
from django.contrib import messages
# Import the custom RegisterForm class from forms.py
from .forms import RegisterForm

# Define the register view function to handle user registration
def register(request):
    # Check if the HTTP request method is POST (meaning the user submitted the form)
    if request.method == 'POST':
        # Instantiate the form with the submitted POST data
        form = RegisterForm(request.POST)
        # Validate the form against the model constraints and custom validations
        if form.is_valid():
            # If valid, save the new user to the database
            form.save()
            # Send a success message to be displayed on the next page
            messages.success(request, 'Account created successfully! You can now log in.')
            # Redirect the user to the login page after successful registration
            return redirect('login')
    # If the request is GET (the user just opened the page)
    else:
        # Instantiate an empty form
        form = RegisterForm()
    # Render the register.html template, passing the form as context data
    return render(request, 'accounts/register.html', {'form': form})

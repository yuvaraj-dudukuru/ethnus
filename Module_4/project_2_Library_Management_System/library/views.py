# Import necessary functions from django.shortcuts for rendering templates, getting objects, and redirecting
from django.shortcuts import render, get_object_or_404, redirect
# Import class-based views for listing, detailing, creating, and updating objects
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# Import decorators to enforce user authentication for specific views
from django.contrib.auth.decorators import login_required, permission_required
# Import mixins for class-based views to enforce authentication and permissions
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Import Q (for complex queries) and F (for database-level operations to avoid race conditions)
from django.db.models import Q, F
# Import timezone utilities (though 'date' is primarily used below)
from django.utils import timezone
# Import the models we created in models.py
from .models import Book, Member, Issue
# Import the custom IssueForm we created in forms.py
from .forms import IssueForm
# Import the date class to handle current dates
from datetime import date

# Create a class-based view to list all books
class BookListView(ListView):
    # Specify the model this view works with
    model = Book
    # Specify the HTML template to use for rendering
    template_name = 'library/book_list.html'
    # Specify the variable name to be used inside the template to access the list
    context_object_name = 'books'

    # Override the default query to add custom search functionality
    def get_queryset(self):
        # Get the default list of books
        qs = super().get_queryset()
        # Retrieve the search query parameter 'q' from the URL (e.g., ?q=harry)
        query = self.request.GET.get('q')
        # If a search query was provided
        if query:
            # Filter the books using Q objects to search across multiple fields (OR logic)
            qs = qs.filter(
                Q(title__icontains=query) |        # Check if title contains the query (case-insensitive)
                Q(author__name__icontains=query) | # Check if author's name contains the query
                Q(isbn__icontains=query)           # Check if ISBN contains the query
            ).distinct()                           # Remove duplicates if multiple conditions match
        # Return the final filtered (or unfiltered) list of books
        return qs

# Create a class-based view to show details of a specific book
class BookDetailView(DetailView):
    # Specify the model
    model = Book
    # Specify the template
    template_name = 'library/book_detail.html'

# Create a class-based view to list all members
class MemberListView(ListView):
    # Specify the model
    model = Member
    # Specify the template
    template_name = 'library/member_list.html'
    # Define the template variable name
    context_object_name = 'members'

# Create a class-based view to show details of a specific member
class MemberDetailView(DetailView):
    # Specify the model
    model = Member
    # Specify the template
    template_name = 'library/member_detail.html'

    # Override get_context_data to pass additional information to the template
    def get_context_data(self, **kwargs):
        # Get the existing context dictionary from the parent class
        context = super().get_context_data(**kwargs)
        # Fetch all issues (borrowed books) related to this specific member
        issues = self.object.issues.all()
        # Calculate the total fine by summing up the fine for each issue
        total_fine = sum(issue.fine for issue in issues)
        # Add the calculated total fine to the context dictionary
        context['total_fine'] = total_fine
        # Add the member's issues to the context dictionary
        context['issues'] = issues
        # Return the updated context
        return context

# Define a function-based view to handle issuing a book, requires the user to be logged in
@login_required
def issue_book(request, book_id):
    # Fetch the book by its Primary Key (ID), or return a 404 error if it doesn't exist
    book = get_object_or_404(Book, pk=book_id)
    # Check if the request is a POST request (meaning the user submitted the form)
    if request.method == 'POST':
        # Bind the submitted data to the IssueForm
        form = IssueForm(request.POST)
        # Check if the book has no available copies
        if not book.is_available:
            # Add a non-field error to the form indicating no copies are available
            form.add_error(None, "No copies available.")
        # If the form is valid (e.g., proper date format, valid member selected)
        elif form.is_valid():
            # Create an issue object from the form but don't save it to the database yet (commit=False)
            issue = form.save(commit=False)
            # Assign the specific book to this issue record
            issue.book = book
            # Now safely save the issue to the database
            issue.save()
            # Atomically decrement the available copies of the book by 1 using F expression
            book.copies_available = F('copies_available') - 1
            # Save only the 'copies_available' field to the database for efficiency
            book.save(update_fields=['copies_available'])
            # Redirect the user back to the book's detail page
            return redirect('library:book_detail', pk=book.pk)
    # If the request is a GET request (e.g., just visiting the page)
    else:
        # Create an empty form instance
        form = IssueForm()
    
    # Render the issue_book template, passing the form and the book object
    return render(request, 'library/issue_book.html', {'form': form, 'book': book})

# Define a function-based view to handle returning a book, requires login
@login_required
def return_book(request, issue_id):
    # Fetch the issue record by its Primary Key (ID), or 404
    issue = get_object_or_404(Issue, pk=issue_id)
    # If the user submitted the return confirmation form
    if request.method == 'POST':
        # Double-check that the book hasn't already been returned
        if not issue.returned:
            # Mark the issue as returned
            issue.returned = True
            # Record today's date as the return date
            issue.return_date = date.today()
            # Save the updated issue record to the database
            issue.save()
            
            # Fetch the associated book from the issue record
            book = issue.book
            # Atomically increment the available copies by 1 using F expression
            book.copies_available = F('copies_available') + 1
            # Save only the 'copies_available' field
            book.save(update_fields=['copies_available'])
            
        # Redirect the user back to the member's detail page
        return redirect('library:member_detail', pk=issue.member.pk)
    # If it's a GET request, render a confirmation page asking if they are sure
    return render(request, 'library/return_book_confirm.html', {'issue': issue})

# Create a class-based view to generate a report of all overdue books
class OverdueReportView(ListView):
    # Specify the model
    model = Issue
    # Specify the template
    template_name = 'library/overdue_report.html'
    # Define the template variable name
    context_object_name = 'issues'

    # Override the default query to only fetch overdue issues
    def get_queryset(self):
        # Filter issues where the book is NOT returned AND the due date is strictly before today
        return Issue.objects.filter(returned=False, due_date__lt=date.today())

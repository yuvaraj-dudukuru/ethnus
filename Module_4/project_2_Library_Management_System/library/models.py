# Import the base models class from django to define our database tables
from django.db import models
# Import the date class from the datetime module to handle dates (like today's date)
from datetime import date

# Define the Author model, which corresponds to the 'library_author' table in the database
class Author(models.Model):
    # Create a character field for the author's name with a maximum length of 120 characters
    name = models.CharField(max_length=120)

    # The string representation method to show the author's name in the Django Admin and templates
    def __str__(self):
        # Return the author's name as the string representation
        return self.name

# Define the Book model, corresponding to the 'library_book' table
class Book(models.Model):
    # A character field for the book's title, max length 120
    title  = models.CharField(max_length=120)
    # A many-to-one relationship (Foreign Key) linking each Book to an Author.
    # on_delete=models.PROTECT prevents an author from being deleted if they have books in the database.
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    # A character field for the ISBN, max length 13, and it must be unique across all books
    isbn   = models.CharField(max_length=13, unique=True)
    # An integer field storing the total number of physical copies the library owns, defaulting to 1
    copies_total = models.PositiveIntegerField(default=1)
    # An integer field storing the number of copies currently available to be issued, defaulting to 1
    copies_available = models.PositiveIntegerField(default=1)
    
    # A computed property (acts like a field but is calculated dynamically) to check availability
    @property
    def is_available(self): 
        # Returns True if there is at least one copy available, otherwise False
        return self.copies_available > 0

    # The string representation of the Book model
    def __str__(self):
        # Return the book's title
        return self.title

# Define the Member model, corresponding to the 'library_member' table
class Member(models.Model):
    # A character field for the member's full name, max length 120
    name = models.CharField(max_length=120)
    # An email field ensuring that each member has a unique email address
    email = models.EmailField(unique=True)
    # A date field that automatically sets the current date when a member is first created
    joined = models.DateField(auto_now_add=True)

    # The string representation of the Member model
    def __str__(self):
        # Return the member's name
        return self.name

# Define the Issue model to track which member borrowed which book
class Issue(models.Model):
    # A Foreign Key linking to the Book model.
    # on_delete=models.CASCADE means if the book is deleted, all its issue records are also deleted.
    # related_name='issues' allows us to access a book's issues backward (e.g., book.issues.all())
    book   = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    
    # A Foreign Key linking to the Member model.
    # CASCADE deletes issue records if the member is deleted.
    # related_name='issues' allows accessing all issues of a member (e.g., member.issues.all())
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='issues')
    
    # A date field automatically set to the day the book was issued
    issue_date  = models.DateField(auto_now_add=True)
    # A date field specifying when the book should be returned
    due_date    = models.DateField()
    # A boolean field indicating whether the book has been returned or not, defaults to False
    returned    = models.BooleanField(default=False)
    # A date field storing when the book was actually returned; allows null and blank values initially
    return_date = models.DateField(null=True, blank=True)
    
    # A computed property to calculate how many days past the due date the issue is
    @property
    def days_overdue(self):
        # If the book has already been returned, it can't be overdue, so return 0
        if self.returned:
            return 0
        # Calculate the difference in days between today's date and the due date
        late = (date.today() - self.due_date).days
        # Return the number of late days, but ensure it doesn't drop below 0 (if not late yet)
        return max(late, 0)
        
    # A computed property to calculate the fine amount
    @property
    def fine(self):
        # Multiply the days overdue by the fine rate (e.g., $5 per day)
        return self.days_overdue * 5

    # The string representation of the Issue model
    def __str__(self):
        # Return a formatted string showing the book title and member name
        return f"{self.book.title} issued to {self.member.name}"

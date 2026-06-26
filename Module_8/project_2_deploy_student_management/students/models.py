# Import the models module from django.db to create database models
from django.db import models

# Define a Department model that inherits from models.Model
class Department(models.Model):
    # Create a character field for the department name, max length 50, and ensure it's unique
    name = models.CharField(max_length=50, unique=True)
    # Define the string representation method for the model
    def __str__(self): 
        # Return the department name when the object is printed
        return self.name

# Define a Student model that inherits from models.Model
class Student(models.Model):
    # Create an integer field for roll number and ensure it is unique across all students
    roll       = models.IntegerField(unique=True)
    # Create a character field for the student's name, max length 50 characters
    name       = models.CharField(max_length=50)
    # Create an email field for the student and ensure the email is unique
    email      = models.EmailField(unique=True)
    # Create an integer field for marks with a default value of 0
    marks      = models.IntegerField(default=0)
    # Create a boolean field to track if the student is active, defaulting to True
    is_active  = models.BooleanField(default=True)
    # Create a date field for admission date that automatically sets to the current date when created
    admitted   = models.DateField(auto_now_add=True)
    # Create an image field for the student's photo, saving to 'students/photos/', and allow it to be blank
    photo      = models.ImageField(upload_to='students/photos/', blank=True)
    # Create a foreign key linking to Department, delete student if department is deleted (CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   # Set the related_name to access students from a department object
                                   related_name='students')
    # Inner Meta class to provide metadata options for the Student model
    class Meta: 
        # Order students by marks in descending order (highest marks first)
        ordering = ['-marks']
    # Define the string representation method for the student object
    def __str__(self): 
        # Return a formatted string showing the roll number and name
        return f"{self.roll} – {self.name}"

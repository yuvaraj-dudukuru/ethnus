# Import the base Model class from django.db.models to define our database tables
from django.db import models
# Import the built-in User model to associate posts and comments with users
from django.contrib.auth.models import User
# Import the reverse function to dynamically generate URLs based on their names
from django.urls import reverse

# Define the Category model to categorize our blog posts
class Category(models.Model):
    # A character field for the category name, with a maximum length of 100 characters
    name = models.CharField(max_length=100)
    # A slug field for URL-friendly category names, which must be unique across the table
    slug = models.SlugField(unique=True)

    # String representation of the Category object, used in the Django admin and templates
    def __str__(self):
        # Return the category name when the object is printed or converted to a string
        return self.name

# Define the Post model to store individual blog posts
class Post(models.Model):
    # A list of tuples defining the choices for the post status (Draft or Published)
    STATUS = [('D', 'Draft'), ('P', 'Published')]
    # A character field for the post title, with a maximum length of 150 characters
    title = models.CharField(max_length=150)
    # A unique slug field for the post, used to create SEO-friendly URLs
    slug = models.SlugField(unique=True)
    # A text field for the main content (body) of the blog post
    body = models.TextField()
    # A character field for the status, limited to 1 character, using the STATUS choices, default is 'Draft'
    status = models.CharField(max_length=1, choices=STATUS, default='D')
    # A date-time field that automatically sets the current time when the post is first created
    created = models.DateTimeField(auto_now_add=True)
    # A foreign key linking the post to a User (author). If the user is deleted, their posts are also deleted (CASCADE)
    # 'related_name' allows us to access all posts by a user using user.posts.all()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    # A foreign key linking the post to a Category. If the category is deleted, this field is set to NULL (SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    # Meta class provides extra information (metadata) about the Post model
    class Meta:
        # Define the default ordering of posts: descending order of creation time (newest first)
        ordering = ['-created']

    # String representation of the Post object
    def __str__(self):
        # Return the post title when the object is converted to a string
        return self.title

    # A method to get the absolute URL of the post detail view
    def get_absolute_url(self):
        # Use reverse to find the URL named 'detail' in the 'blog' app namespace, passing the post's slug
        return reverse('blog:detail', kwargs={'slug': self.slug})

# Define the Comment model to allow users to comment on posts
class Comment(models.Model):
    # A foreign key linking the comment to a specific Post. If the post is deleted, the comment is deleted (CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # A foreign key linking the comment to a User. If the user is deleted, their comments are deleted (CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # A text field for the content of the comment
    body = models.TextField()
    # A date-time field that automatically sets the current time when the comment is created
    created = models.DateTimeField(auto_now_add=True)

    # Meta class for the Comment model metadata
    class Meta:
        # Define the default ordering of comments: ascending order of creation time (oldest first)
        ordering = ['created']

    # String representation of the Comment object
    def __str__(self):
        # Return a formatted string indicating who made the comment and on which post
        return f"Comment by {self.user.username} on {self.post.title}"

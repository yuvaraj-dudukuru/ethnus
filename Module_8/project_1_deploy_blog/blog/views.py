# Import the render function to render HTML templates
from django.shortcuts import render, get_object_or_404, redirect
# Import Django's generic class-based views for listing, detailing, creating, and updating objects
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# Import mixins to enforce user authentication and custom permission checks for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Import the login_required decorator to restrict access to function-based views
from django.contrib.auth.decorators import login_required
# Import our custom database models: Post, Category, and Comment
from .models import Post, Category, Comment
# Import our custom forms for handling form validation and saving data
from .forms import CommentForm, PostForm
# Import reverse_lazy for safely reversing URLs during class loading
from django.urls import reverse_lazy

# Define a view to display a list of all published posts
class PostListView(ListView):
    # Specify the model this view will work with
    model = Post
    # Specify the HTML template to use for rendering the page
    template_name = 'blog/post_list.html'
    # Define the variable name to be used inside the template to access the list of objects
    context_object_name = 'posts'

    # Override the default queryset to only fetch posts with 'Published' status
    def get_queryset(self):
        # Return a filtered queryset where status equals 'P'
        return Post.objects.filter(status='P')

# Define a view to display a list of posts belonging to a specific category
class CategoryPostListView(ListView):
    # Specify the model this view will work with
    model = Post
    # Specify the HTML template to use for rendering the page
    template_name = 'blog/category_list.html'
    # Define the variable name for the template context
    context_object_name = 'posts'

    # Override the default queryset to filter posts by the category slug from the URL
    def get_queryset(self):
        # Extract the 'slug' parameter passed from the URL
        category_slug = self.kwargs.get('slug')
        # Fetch the category object matching the slug, or return a 404 error if it doesn't exist
        self.category = get_object_or_404(Category, slug=category_slug)
        # Return posts that are both published and belong to the fetched category
        return Post.objects.filter(status='P', category=self.category)

    # Override the context data method to pass extra variables to the template
    def get_context_data(self, **kwargs):
        # Get the default context dictionary from the parent class
        context = super().get_context_data(**kwargs)
        # Add the current category object to the context dictionary
        context['category'] = self.category
        # Return the updated context dictionary
        return context

# Define a view to display the details of a single post
class PostDetailView(DetailView):
    # Specify the model this view will work with
    model = Post
    # Specify the HTML template to use for rendering the page
    template_name = 'blog/post_detail.html'
    # Define the variable name for the template context (representing the single post)
    context_object_name = 'post'

    # Override the context data method to pass comments and the comment form
    def get_context_data(self, **kwargs):
        # Get the default context dictionary from the parent class
        context = super().get_context_data(**kwargs)
        # Initialize an empty CommentForm and add it to the context for the template
        context['comment_form'] = CommentForm()
        # Fetch all comments related to this post and add them to the context
        context['comments'] = self.object.comments.all()
        # Return the updated context dictionary
        return context

# Define a view to create a new post, requiring the user to be logged in
class PostCreateView(LoginRequiredMixin, CreateView):
    # Specify the model to create
    model = Post
    # Specify the custom form class to use for input validation
    form_class = PostForm
    # Specify the HTML template to render the form
    template_name = 'blog/post_form.html'
    
    # Override the form_valid method which is called when valid form data has been POSTed
    def form_valid(self, form):
        # Stamp the current logged-in user as the author of the new post instance before saving
        form.instance.author = self.request.user
        # Call the parent class's form_valid method to actually save the post and redirect
        return super().form_valid(form)

# Define a view to update an existing post, requiring login and a specific permission test
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Specify the model to update
    model = Post
    # Specify the custom form class to use for editing
    form_class = PostForm
    # Specify the HTML template to render the form
    template_name = 'blog/post_form.html'

    # Implement the test_func required by UserPassesTestMixin to check permissions
    def test_func(self):
        # Return True only if the author of the post being edited is the currently logged-in user
        return self.get_object().author == self.request.user

# Define a view for the author's dashboard, requiring the user to be logged in
class AuthorDashboardView(LoginRequiredMixin, ListView):
    # Specify the model to query
    model = Post
    # Specify the HTML template to render the dashboard
    template_name = 'blog/dashboard.html'
    # Define the variable name for the template context
    context_object_name = 'posts'

    # Override the get_queryset method to fetch only the current user's posts
    def get_queryset(self):
        # Filter all posts (both Draft and Published) authored by the logged-in user
        return Post.objects.filter(author=self.request.user)

# Use a decorator to ensure only logged-in users can execute this function-based view
@login_required
# Define a function-based view to handle the submission of a new comment
def add_comment(request, slug):
    # Fetch the published post matching the provided slug, or return a 404 error
    post = get_object_or_404(Post, slug=slug, status='P')
    # Check if the HTTP request method is POST (which means form data was submitted)
    if request.method == 'POST':
        # Create a CommentForm instance populated with the submitted POST data
        form = CommentForm(request.POST)
        # Validate the submitted form data
        if form.is_valid():
            # Save the form data to an object, but don't commit it to the database just yet
            c = form.save(commit=False)
            # Link the newly created comment object to the specific post
            c.post = post
            # Link the newly created comment object to the currently logged-in user
            c.user = request.user
            # Now save the completely populated comment object to the database
            c.save()
    # After processing the comment, redirect the user back to the post's detail page
    return redirect('blog:detail', slug=slug)

# Import the basic models module from django to define our database tables
from django.db import models
# Import the built-in User model for authentication and tying orders to users
from django.contrib.auth.models import User
# Import reverse function to generate URLs based on their names in urls.py
from django.urls import reverse

# Define the Category model to group our products
class Category(models.Model):
    # The name of the category, max 200 characters, indexed for fast database lookups
    name = models.CharField(max_length=200, db_index=True)
    # The slug for the category, used in SEO-friendly URLs, must be unique across all categories
    slug = models.SlugField(max_length=200, unique=True)

    # Meta class provides metadata to the model
    class Meta:
        # Default ordering is alphabetical by name
        ordering = ('name',)
        # Singular human-readable name in the admin panel
        verbose_name = 'category'
        # Plural human-readable name in the admin panel
        verbose_name_plural = 'categories'

    # The string representation of the model instance (how it shows in admin)
    def __str__(self):
        # Return the category's name
        return self.name

    # Helper method to get the absolute URL for a category instance
    def get_absolute_url(self):
        # Generates a URL for 'store:product_list_by_category' using the category slug
        return reverse('store:product_list_by_category', args=[self.slug])


# Define the Product model representing items for sale
class Product(models.Model):
    # Foreign key linking the product to a Category (1-to-Many relationship)
    # on_delete=models.CASCADE means deleting a category deletes its products
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    # The name of the product, max 200 chars, indexed for fast database lookups
    name = models.CharField(max_length=200, db_index=True)
    # SEO-friendly URL string for the product
    slug = models.SlugField(max_length=200, db_index=True)
    # Image field for product photo, uploads to 'products/YYYY/MM/DD', blank=True means it's optional
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    # Long text description of the product, blank=True means it's optional
    description = models.TextField(blank=True)
    # Decimal field for price, max 8 digits total, 2 decimal places (crucial for accurate money math)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # Integer field to track how many items are in stock, defaults to 0
    stock = models.PositiveIntegerField(default=0)
    # Boolean field to easily toggle product visibility on the site
    available = models.BooleanField(default=True)
    # Automatically stores the date/time when the product is created
    created = models.DateTimeField(auto_now_add=True)
    # Automatically updates the date/time whenever the product is saved
    updated = models.DateTimeField(auto_now=True)

    # Metadata for the Product model
    class Meta:
        # Order products by name alphabetically
        ordering = ('name',)
        # Creates a composite database index on id and slug for fast multi-column lookups
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    # String representation of the product
    def __str__(self):
        # Returns the product name
        return self.name

    # Helper method to get the URL for the product detail page
    def get_absolute_url(self):
        # Generates a URL matching 'store:product_detail' using product id and slug
        return reverse('store:product_detail', args=[self.id, self.slug])


# Define the Order model to represent a customer's purchase
class Order(models.Model):
    # Tuple containing choices for the order's current status
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    # Link the order to the User who made it. Deleting a user deletes their orders.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    # Automatically records when the order was placed
    created = models.DateTimeField(auto_now_add=True)
    # Stores the total cost of the order, default is 0
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Stores the status of the order, defaults to 'Pending', choices restricted to STATUS_CHOICES
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Metadata for the Order model
    class Meta:
        # Sort orders by creation date in descending order (newest first)
        ordering = ('-created',)

    # String representation for the Order
    def __str__(self):
        # Returns a string like "Order 5"
        return f'Order {self.id}'

    # Helper method to calculate the total cost by summing all item costs
    def get_total_cost(self):
        # Sum up the result of get_cost() for each related OrderItem
        return sum(item.get_cost() for item in self.items.all())


# Define OrderItem model to link individual products to an Order
class OrderItem(models.Model):
    # Link to the Order. If an order is deleted, its items are deleted too.
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Link to the Product being purchased
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    # How many units of the product were bought, defaults to 1
    qty = models.PositiveIntegerField(default=1)
    # PRICE SNAPSHOT: Stores the product's price at the exact moment of checkout.
    # This ensures that if the product price changes later, the order history isn't affected.
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)

    # String representation of the OrderItem
    def __str__(self):
        # Returns the ID of the OrderItem as a string
        return str(self.id)

    # Helper method to get the total cost for this line item
    def get_cost(self):
        # Multiplies the locked-in purchase price by the quantity bought
        return self.price_at_purchase * self.qty

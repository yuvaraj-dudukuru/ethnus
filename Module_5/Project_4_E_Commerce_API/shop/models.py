# ============================================================================
#  models.py — the database design (extended from Module-4 Project 4)
# ----------------------------------------------------------------------------
#  Tables and how they connect:
#
#      Category 1 ───< N Product
#      User 1 ──O2O── 1 Cart 1 ───< N CartItem >─── N 1 Product
#      User 1 ───< N Order 1 ───< N OrderItem >─── N 1 Product
#
#  WHY A CART MODEL NOW?  In Module 4 the cart lived in the browser SESSION.
#  But our API uses TOKENS, which are STATELESS — there is no session "bag" to
#  stash a cart in. So the cart must become real database rows, keyed to the
#  user. That is exactly how real online shops do it. (Good viva point!)
#
#  MONEY CORRECTNESS:  prices use DecimalField (NOT float). Floats can't store
#  money exactly (0.1 + 0.2 != 0.3 in float). Decimal stores exact rupees and
#  paise, so totals always add up correctly.
# ============================================================================
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """A product category, e.g. 'Electronics' or 'Books'."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    """One item for sale in the catalog."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Exact money value: up to 99,999,999.99.
    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )

    # The catalog is paginated with CursorPagination, which needs a stable,
    # ordered field to page through. 'created' is perfect for that.
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']   # newest products first

    def __str__(self):
        return self.name


class Cart(models.Model):
    """A user's shopping cart. OneToOne = each user has exactly ONE cart."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.user}"


class CartItem(models.Model):
    """One line in a cart: a product and how many of it."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        # A product appears at most once per cart (we update qty instead of
        # adding a duplicate row).
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.qty} x {self.product}"


class Order(models.Model):
    """A placed order — created at checkout from the contents of the cart."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    # The grand total, computed and frozen at checkout time.
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class OrderItem(models.Model):
    """One line in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()

    # SNAPSHOT of the price at the moment of purchase. We copy the price into
    # the order line so that if the shop changes the product's price LATER,
    # this historical order still shows what the customer actually paid.
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.qty} x {self.product} @ {self.price_at_purchase}"

# ============================================================================
#  models.py — products, suppliers and an audit trail of stock movements.
# ----------------------------------------------------------------------------
#  Category 1 ─< N Product >─ N 1 Supplier
#  Product  1 ─< N StockMovement   (every IN/OUT is recorded for auditing)
# ============================================================================
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    contact = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=40, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products")
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["name"]

    @property
    def low_stock(self):
        return self.quantity <= self.reorder_level

    def __str__(self):
        return f"{self.name} ({self.sku})"


class StockMovement(models.Model):
    TYPES = [("IN", "Stock in"), ("OUT", "Stock out")]
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="movements")
    type = models.CharField(max_length=3, choices=TYPES)
    qty = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.type} {self.qty} × {self.product.name}"

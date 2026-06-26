# ============================================================================
#  admin.py — register our models with Django's built-in admin panel
# ----------------------------------------------------------------------------
#  Makes everything editable at http://127.0.0.1:8000/admin/ with a ready-made
#  web interface (log in as admin / admin).
# ============================================================================
from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock', 'category', 'created']
    list_filter = ['category']
    search_fields = ['name', 'description']


# Show the items right inside the order/cart edit page.
class CartItemInline(admin.TabularInline):
    model = CartItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    inlines = [CartItemInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'created']
    inlines = [OrderItemInline]

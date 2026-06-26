from django.contrib import admin
from .models import Category, Product, Order, OrderItem

# Registering Category with prepopulated slug
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Registering Product with list_editable for quick stock management
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']  # Stock and price can be edited in the list view
    prepopulated_fields = {'slug': ('name',)}

# Inline for OrderItem to show inside Order admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

# Registering Order with the OrderItem inline
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total', 'created']
    list_filter = ['status', 'created']
    inlines = [OrderItemInline]

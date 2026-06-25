# ============================================================================
#  serializers.py — translators between database objects and JSON
# ----------------------------------------------------------------------------
#  The star of this file is OrderCreateSerializer: a TRANSACTIONAL serializer
#  that turns the user's cart into a real order, all-or-nothing.
# ============================================================================
from django.db import transaction
from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    """The shape of a Product in the catalog."""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock',
                  'category', 'category_name', 'created']
        read_only_fields = ['created']


# ----------------------------- CART -----------------------------------------

class CartItemSerializer(serializers.ModelSerializer):
    """One line of the cart, with a computed line total (price x qty)."""
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'price', 'qty', 'line_total']

    def get_line_total(self, obj):
        # Decimal math keeps money exact.
        return obj.product.price * obj.qty


class CartSerializer(serializers.ModelSerializer):
    """The whole cart: all its items plus a computed grand total."""
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total']

    def get_total(self, obj):
        return sum((i.product.price * i.qty for i in obj.items.all()), 0)


class AddCartItemSerializer(serializers.Serializer):
    """Validates the body of POST /api/cart/items/  ->  {product, qty}."""
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    qty = serializers.IntegerField(min_value=1)


# ----------------------------- ORDERS ---------------------------------------

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'qty', 'price_at_purchase']


class OrderSerializer(serializers.ModelSerializer):
    """The shape used to DISPLAY an order (with its lines)."""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'created', 'items']
        read_only_fields = fields   # orders are never edited through this serializer


class OrderCreateSerializer(serializers.Serializer):
    """CHECKOUT: build an Order from the logged-in user's cart.

    This is a transactional serializer. The whole thing runs inside
    transaction.atomic(): if ANY step fails, the database is rolled back and no
    half-finished order is left behind. That is essential for money correctness.
    """

    def create(self, validated_data):
        user = self.context['request'].user

        # Pull the cart and its items efficiently (one query for the lines).
        cart = Cart.objects.prefetch_related('items__product').get(user=user)
        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty.")

        with transaction.atomic():            # all-or-nothing
            order = Order.objects.create(user=user, total=0)
            total = 0
            for ci in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=ci.product,
                    qty=ci.qty,
                    price_at_purchase=ci.product.price,   # snapshot the price!
                )
                total += ci.product.price * ci.qty
            order.total = total
            order.save()
            # Empty the cart now that everything has been ordered.
            cart.items.all().delete()
        return order

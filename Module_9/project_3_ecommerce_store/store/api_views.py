# ============================================================================
#  api_views.py — catalog, cart and transactional checkout.
# ----------------------------------------------------------------------------
#  Checkout is wrapped in transaction.atomic(): either the WHOLE order is
#  created (price snapshots written, stock decremented, cart emptied) or NOTHING
#  is — there is no half-finished order if something fails midway.
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F

from .filters import ProductFilter
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer,
)


class ProductCursorPagination(CursorPagination):
    """Cursor pagination scales to huge catalogs (no expensive COUNT/OFFSET)."""
    page_size = 12
    ordering = "-id"


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    """Browse products (public). Only admins create/edit/delete."""
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ProductCursorPagination
    filterset_class = ProductFilter
    search_fields = ["name", "description", "category__name"]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return super().get_permissions()


class CartViewSet(viewsets.ViewSet):
    """The current user's cart. Every action is private to that user."""
    permission_classes = [IsAuthenticated]

    def _cart(self):
        return Cart.objects.get_or_create(user=self.request.user)[0]

    def list(self, request):
        return Response(CartSerializer(self._cart()).data)

    @action(detail=False, methods=["post"])
    def add(self, request):
        """POST /api/cart/add/  body: {"product_id": 1, "qty": 2}."""
        product = Product.objects.filter(pk=request.data.get("product_id")).first()
        if product is None:
            return Response({"detail": "Invalid product_id."}, status=400)
        qty = int(request.data.get("qty", 1))
        cart = self._cart()
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.qty = qty if created else item.qty + qty
        if item.qty > product.stock:
            return Response({"detail": "Not enough stock."}, status=400)
        item.save()
        return Response(CartSerializer(cart).data, status=200)

    @action(detail=False, methods=["post"])
    def remove(self, request):
        """POST /api/cart/remove/  body: {"product_id": 1}."""
        cart = self._cart()
        CartItem.objects.filter(
            cart=cart, product_id=request.data.get("product_id")).delete()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        """POST /api/cart/checkout/ — turn the cart into a paid order."""
        cart = self._cart()
        items = list(cart.items.select_related("product"))
        if not items:
            return Response({"detail": "Your cart is empty."}, status=400)

        with transaction.atomic():
            # 1) Validate stock for every line first.
            for it in items:
                if it.product.stock < it.qty:
                    return Response(
                        {"detail": f"Not enough stock for {it.product.name}."},
                        status=400)
            # 2) Create the order, snapshot prices, decrement stock atomically.
            order = Order.objects.create(user=request.user, total=0)
            total = 0
            for it in items:
                OrderItem.objects.create(
                    order=order, product=it.product, product_name=it.product.name,
                    qty=it.qty, price_at_purchase=it.product.price)
                Product.objects.filter(pk=it.product.pk).update(
                    stock=F("stock") - it.qty)
                total += it.product.price * it.qty
            order.total = total
            order.save()
            # 3) Empty the cart.
            cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=201)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Order history. Customers see ONLY their own orders (IDOR-safe)."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Order.objects.prefetch_related("items")
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            qs = qs.filter(user=user)
        return qs

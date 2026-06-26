# ============================================================================
#  api_views.py — catalog, atomic stock movements and low-stock alerts.
# ----------------------------------------------------------------------------
#  stock_in / stock_out change the quantity with an ATOMIC F() update and log a
#  StockMovement, so the running total can never be corrupted by two clerks
#  updating the same product at once.
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F

from .filters import ProductFilter
from .models import Category, Supplier, Product, StockMovement
from .serializers import (
    CategorySerializer, SupplierSerializer, ProductSerializer,
    StockMovementSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ["name", "contact"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category", "supplier")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = ProductFilter
    search_fields = ["name", "sku", "category__name", "supplier__name"]
    ordering_fields = ["name", "quantity", "price"]

    def get_permissions(self):
        # Creating/editing the catalog itself is an admin/manager job.
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdminUser()]
        return super().get_permissions()

    def _move(self, request, sign):
        qty = int(request.data.get("qty", 0))
        if qty <= 0:
            return None, Response({"detail": "qty must be positive."}, status=400)
        product = self.get_object()
        with transaction.atomic():
            if sign < 0:
                changed = (Product.objects
                           .filter(pk=product.pk, quantity__gte=qty)
                           .update(quantity=F("quantity") - qty))
                if not changed:
                    return None, Response(
                        {"detail": "Not enough stock."}, status=400)
            else:
                Product.objects.filter(pk=product.pk).update(
                    quantity=F("quantity") + qty)
            StockMovement.objects.create(
                product=product, type=("IN" if sign > 0 else "OUT"),
                qty=qty, note=request.data.get("note", ""))
        product.refresh_from_db()
        return product, None

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def stock_in(self, request, pk=None):
        """POST /api/products/<id>/stock_in/  body: {"qty": 10, "note": "..."}."""
        product, err = self._move(request, +1)
        return err or Response(ProductSerializer(product).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def stock_out(self, request, pk=None):
        """POST /api/products/<id>/stock_out/  body: {"qty": 3, "note": "..."}."""
        product, err = self._move(request, -1)
        return err or Response(ProductSerializer(product).data)

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """GET /api/products/low_stock/ — products at/under their reorder level."""
        qs = self.get_queryset().filter(quantity__lte=F("reorder_level"))
        return Response(self.get_serializer(qs, many=True).data)


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only audit log of every stock change."""
    queryset = StockMovement.objects.select_related("product")
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["product", "type"]

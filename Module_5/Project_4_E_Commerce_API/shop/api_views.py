# ============================================================================
#  api_views.py — the API's "brains": what happens on each request
# ----------------------------------------------------------------------------
#  This file shows the four new "muscles" of Project 4:
#    1) The CART as a real API resource (user-keyed rows, no sessions).
#    2) CHECKOUT as a transactional create (OrderCreateSerializer).
#    3) Owner-scoped get_queryset() -> the IDOR-proof "you only see your own".
#    4) CursorPagination on the big, live product catalog.
# ============================================================================
from rest_framework import viewsets, mixins, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Cart, CartItem, Order
from .serializers import (
    ProductSerializer, CartSerializer, AddCartItemSerializer,
    OrderSerializer, OrderCreateSerializer,
)
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly
from .pagination import ProductCursorPagination


class ProductViewSet(viewsets.ModelViewSet):
    """The product catalog: public to read, admin-only to change.

    Uses CursorPagination because a real shop catalog is large and changes
    while customers browse.
    """
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ProductCursorPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']   # ?search=phone
    ordering_fields = ['price', 'created']    # ?ordering=price


# A tiny helper so every cart view fetches (or creates) the user's cart safely.
def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(APIView):
    """GET /api/cart/  -> view my cart   •   DELETE /api/cart/ -> empty my cart.

    The cart is strictly per-user: we always look it up by request.user, so you
    can only ever see or clear YOUR OWN cart.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = _get_cart(request.user)
        return Response(CartSerializer(cart).data)

    def delete(self, request):
        cart = _get_cart(request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemsView(APIView):
    """POST /api/cart/items/  -> add or update a line   {product, qty}
       DELETE /api/cart/items/ -> remove a line          {product}
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = AddCartItemSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        product = ser.validated_data['product']
        qty = ser.validated_data['qty']

        cart = _get_cart(request.user)
        # If this product is already in the cart, update its quantity;
        # otherwise create a new line.
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={'qty': qty}
        )
        if not created:
            item.qty = qty
            item.save()
        code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(CartSerializer(cart).data, status=code)

    def delete(self, request):
        product_id = request.data.get('product')
        cart = _get_cart(request.user)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response(CartSerializer(cart).data)


class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """Orders: list/retrieve your OWN, and create one by CHECKING OUT.

    There is no update/delete — an order, once placed, is history.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ⭐ THE IDOR-PROOF PATTERN: only ever return THIS user's orders. Even
        # if someone guesses another order's id, it isn't in this queryset, so
        # they get a 404 instead of someone else's data.
        return (Order.objects
                .filter(user=self.request.user)
                .prefetch_related('items__product'))

    def get_serializer_class(self):
        # Use the transactional checkout serializer for create, the display
        # serializer for everything else.
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """POST /api/orders/  ->  CHECKOUT: turn my cart into an order."""
        ser = OrderCreateSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        order = ser.save()
        # Respond with the full, freshly created order.
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class LogoutAPI(APIView):
    """POST /api/logout/ — log the current user out by deleting their token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth is not None:
            request.auth.delete()
        return Response(status=204)   # 204 = success, nothing to send back

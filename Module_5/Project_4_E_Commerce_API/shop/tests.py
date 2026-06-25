# ============================================================================
#  tests.py — automated checks for the two trickiest business rules
# ----------------------------------------------------------------------------
#  Run every test with:   python manage.py test
#
#  We test:
#    1) Checkout creates an order with the right total AND empties the cart.
#    2) The price SNAPSHOT survives a later price change (the order still shows
#       the price the customer actually paid).
#
#  Each test uses a temporary throwaway database, so real data is never touched.
# ============================================================================
from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from shop.models import Category, Product, Cart, CartItem, Order, OrderItem


class CheckoutTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('shopper', password='pass12345')
        self.cat = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Phone', price=Decimal('100.00'), stock=10, category=self.cat,
        )
        # Give the shopper a cart with 2 phones in it.
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, qty=2)

    def test_checkout_empties_cart_and_totals(self):
        self.client.force_authenticate(self.user)
        r = self.client.post('/api/orders/')   # POST = checkout

        # An order was created...
        self.assertEqual(r.status_code, 201)
        # ...with the correct total (2 x 100.00 = 200.00)...
        self.assertEqual(Decimal(r.data['total']), Decimal('200.00'))
        # ...and the cart is now empty.
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_price_snapshot_survives_price_change(self):
        self.client.force_authenticate(self.user)
        self.client.post('/api/orders/')   # checkout at price 100.00

        # The shop later RAISES the price.
        self.product.price = Decimal('999.00')
        self.product.save()

        # The order line must still show the OLD price the customer paid.
        item = OrderItem.objects.get()
        self.assertEqual(item.price_at_purchase, Decimal('100.00'))

    def test_checkout_with_empty_cart_is_rejected(self):
        # A user with an empty cart cannot check out.
        other = User.objects.create_user('empty', password='pass12345')
        Cart.objects.create(user=other)
        self.client.force_authenticate(other)
        r = self.client.post('/api/orders/')
        self.assertEqual(r.status_code, 400)

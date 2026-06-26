# ============================================================================
#  tests.py — E-Commerce API checks.  Run with:  python manage.py test
# ============================================================================
from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Category, Product, Order


class StoreAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@shop.test", "admin")
        self.u1 = User.objects.create_user("buyer1", password="buyer")
        self.u2 = User.objects.create_user("buyer2", password="buyer")
        self.cat = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            name="Widget", price=Decimal("10.00"), stock=5, category=self.cat)

    def test_public_can_list_products(self):
        self.assertEqual(self.client.get("/api/products/").status_code, 200)

    def test_add_to_cart_requires_login(self):
        r = self.client.post("/api/cart/add/", {"product_id": self.product.id})
        self.assertEqual(r.status_code, 401)

    def test_checkout_creates_order_and_decrements_stock(self):
        self.client.force_authenticate(self.u1)
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "qty": 2})
        r = self.client.post("/api/cart/checkout/")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(float(r.data["total"]), 20.0)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        # Cart is now empty.
        cart = self.client.get("/api/cart/")
        self.assertEqual(cart.data["count"], 0)

    def test_price_snapshot_survives_price_change(self):
        self.client.force_authenticate(self.u1)
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "qty": 2})
        order = self.client.post("/api/cart/checkout/").data
        # Price goes up AFTER the purchase.
        self.product.price = Decimal("99.00")
        self.product.save()
        again = self.client.get(f"/api/orders/{order['id']}/")
        self.assertEqual(float(again.data["items"][0]["price_at_purchase"]), 10.0)

    def test_checkout_empty_cart_is_rejected(self):
        self.client.force_authenticate(self.u1)
        self.assertEqual(self.client.post("/api/cart/checkout/").status_code, 400)

    def test_orders_are_owner_scoped(self):
        self.client.force_authenticate(self.u1)
        self.client.post("/api/cart/add/", {"product_id": self.product.id, "qty": 1})
        self.client.post("/api/cart/checkout/")
        # A different user must NOT see user1's order.
        self.client.force_authenticate(self.u2)
        r = self.client.get("/api/orders/")
        self.assertEqual(r.data["count"], 0)

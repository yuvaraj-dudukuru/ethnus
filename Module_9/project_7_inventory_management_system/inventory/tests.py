# ============================================================================
#  tests.py — Inventory API checks.  Run with:  python manage.py test
# ============================================================================
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Category, Product, StockMovement


class InventoryAPITests(APITestCase):
    def setUp(self):
        self.staff = User.objects.create_user("clerk", password="x")
        self.admin = User.objects.create_superuser("admin", "a@inv.test", "admin")
        self.cat = Category.objects.create(name="Hardware")
        self.product = Product.objects.create(
            name="Bolt", sku="BOLT-1", category=self.cat,
            quantity=10, reorder_level=5)

    def test_public_can_list_products(self):
        self.assertEqual(self.client.get("/api/products/").status_code, 200)

    def test_stock_in_increases_quantity_and_logs_movement(self):
        self.client.force_authenticate(self.staff)
        r = self.client.post(f"/api/products/{self.product.id}/stock_in/",
                             {"qty": 5, "note": "delivery"})
        self.assertEqual(r.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 15)
        self.assertEqual(StockMovement.objects.filter(type="IN").count(), 1)

    def test_stock_out_cannot_go_negative(self):
        self.client.force_authenticate(self.staff)
        r = self.client.post(f"/api/products/{self.product.id}/stock_out/", {"qty": 999})
        self.assertEqual(r.status_code, 400)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)            # unchanged
        self.assertEqual(StockMovement.objects.count(), 0)     # no phantom log

    def test_low_stock_detection(self):
        Product.objects.create(name="Nut", sku="NUT-1", category=self.cat,
                               quantity=2, reorder_level=5)        # low
        r = self.client.get("/api/products/low_stock/")
        skus = {p["sku"] for p in r.data}
        self.assertIn("NUT-1", skus)
        self.assertNotIn("BOLT-1", skus)

    def test_movement_audit_trail(self):
        self.client.force_authenticate(self.staff)
        self.client.post(f"/api/products/{self.product.id}/stock_in/", {"qty": 3})
        self.client.post(f"/api/products/{self.product.id}/stock_out/", {"qty": 1})
        types = list(StockMovement.objects.order_by("date").values_list("type", flat=True))
        self.assertEqual(types, ["IN", "OUT"])

    def test_only_admin_can_create_product(self):
        self.client.force_authenticate(self.staff)
        r = self.client.post("/api/products/", {
            "name": "Screw", "sku": "SCR-1", "category_id": self.cat.id})
        self.assertEqual(r.status_code, 403)

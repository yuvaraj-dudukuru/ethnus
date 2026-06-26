# ============================================================================
#  seed.py — admin/admin + a clerk + sample categories, suppliers, products.
#      python manage.py seed
# ============================================================================
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from inventory.models import Category, Supplier, Product


class Command(BaseCommand):
    help = "Create admin/admin, clerk1/clerk and sample inventory."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@inv.test", "admin")
        if not User.objects.filter(username="clerk1").exists():
            User.objects.create_user("clerk1", password="clerk")
        self.stdout.write(self.style.SUCCESS("Users: admin/admin, clerk1/clerk."))

        hw, _ = Category.objects.get_or_create(name="Hardware")
        el, _ = Category.objects.get_or_create(name="Electronics")
        acme, _ = Supplier.objects.get_or_create(
            name="Acme Supplies", defaults={"contact": "sales@acme.test"})
        glob, _ = Supplier.objects.get_or_create(
            name="Globex", defaults={"contact": "orders@globex.test"})

        rows = [
            ("Hex Bolt M6", "BOLT-M6", hw, acme, 120, 30, "0.15"),
            ("Wood Screw 40mm", "SCR-40", hw, acme, 8, 25, "0.05"),    # low
            ("AA Battery", "BAT-AA", el, glob, 60, 40, "0.50"),
            ("USB Cable", "USB-C1", el, glob, 4, 10, "3.20"),          # low
        ]
        for name, sku, cat, sup, qty, reorder, price in rows:
            Product.objects.get_or_create(
                sku=sku, defaults={"name": name, "category": cat, "supplier": sup,
                                   "quantity": qty, "reorder_level": reorder,
                                   "price": Decimal(price)})

        self.stdout.write(self.style.SUCCESS(
            "Seeded inventory (two items start LOW). Run: python manage.py runserver"))

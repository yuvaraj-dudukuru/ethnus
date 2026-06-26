# ============================================================================
#  seed.py — admin/admin + a demo shopper + sample catalog.
#      python manage.py seed
# ============================================================================
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from store.models import Category, Product


class Command(BaseCommand):
    help = "Create admin/admin, a demo shopper and sample products."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@shop.test", "admin")
            self.stdout.write(self.style.SUCCESS("Created admin/admin."))
        if not User.objects.filter(username="shopper1").exists():
            User.objects.create_user("shopper1", password="shopper")
            self.stdout.write(self.style.SUCCESS("Created shopper1/shopper."))

        electronics, _ = Category.objects.get_or_create(name="Electronics")
        books, _ = Category.objects.get_or_create(name="Books")
        home, _ = Category.objects.get_or_create(name="Home")

        rows = [
            ("Wireless Mouse", "Comfortable 2.4GHz mouse", "19.99", 40, electronics),
            ("Mechanical Keyboard", "Clicky switches", "59.99", 25, electronics),
            ("USB-C Hub", "7-in-1 adapter", "34.50", 15, electronics),
            ("Clean Code", "A handbook of craftsmanship", "29.00", 30, books),
            ("The Pragmatic Programmer", "Classic dev book", "32.00", 12, books),
            ("Ceramic Mug", "350ml, dishwasher safe", "9.99", 100, home),
        ]
        for name, desc, price, stock, cat in rows:
            Product.objects.get_or_create(
                name=name,
                defaults={"description": desc, "price": Decimal(price),
                          "stock": stock, "category": cat})

        self.stdout.write(self.style.SUCCESS(
            "Seeded categories and products. Run: python manage.py runserver"))

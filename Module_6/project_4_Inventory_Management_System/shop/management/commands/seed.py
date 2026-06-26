# ============================================================================
#  seed.py — one-command setup helper:  python manage.py seed
# ----------------------------------------------------------------------------
#  Sets up everything you need to start playing with the API:
#
#     1) An admin account    -> username "admin",   password "admin"
#        (admin/staff can add/edit products)
#     2) A normal shopper    -> username "shopper", password "shopper"
#        (use this one to fill a cart and check out)
#     3) Sample categories and products to browse.
#
#  Safe to run more than once (uses get_or_create). Run it right after migrate.
# ============================================================================
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Create admin + shopper accounts and some sample products."

    def handle(self, *args, **options):
        # --- 1) The admin (superuser): admin / admin ---
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@shop.test', 'admin')
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin)."))
        else:
            self.stdout.write("Admin user already exists — skipping.")

        # --- 2) A normal shopper: shopper / shopper ---
        shopper, created = User.objects.get_or_create(
            username='shopper', defaults={'email': 'shopper@shop.test'}
        )
        if created:
            shopper.set_password('shopper')
            shopper.save()
            self.stdout.write(self.style.SUCCESS("Created shopper user (shopper / shopper)."))

        # --- 3) Sample categories and products ---
        electronics, _ = Category.objects.get_or_create(name='Electronics')
        books, _ = Category.objects.get_or_create(name='Books')

        sample_products = [
            ('Smartphone',   Decimal('299.99'), 50, electronics),
            ('Headphones',   Decimal('49.99'),  200, electronics),
            ('Laptop',       Decimal('899.00'), 20, electronics),
            ('Python Book',  Decimal('19.99'),  100, books),
            ('Django Book',  Decimal('24.50'),  80, books),
        ]
        for name, price, stock, cat in sample_products:
            Product.objects.get_or_create(
                name=name,
                defaults={'price': price, 'stock': stock, 'category': cat},
            )

        self.stdout.write(self.style.SUCCESS(
            "Sample categories and products are ready. "
            "Start the server with: python manage.py runserver"
        ))

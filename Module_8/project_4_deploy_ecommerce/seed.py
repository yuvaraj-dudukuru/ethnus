"""
seed.py - One-off database seeding script for the E-commerce mini store.

Run ``python seed.py`` to create:
  * an administrator account (username: admin, password: admin), and
  * two categories (Electronics, Clothing) with four sample products.

The script is idempotent: it checks for existing rows before creating, so you
can run it as many times as you like without producing duplicates.
"""

# Standard library: environment variables.
import os
# Django framework, bootstrapped manually because this is a standalone script.
import django

# Point Django at the settings module, then initialise the framework.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

# Import models only AFTER django.setup() has run.
from django.contrib.auth.models import User
from store.models import Category, Product


def seed_data():
    """Create the admin account plus a small catalogue of demo products."""
    print("Creating superuser admin/admin...")
    # create_superuser() bypasses the password validators, so "admin" is allowed.
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    print("Creating categories...")
    electronics, _ = Category.objects.get_or_create(name='Electronics', slug='electronics')
    clothing, _ = Category.objects.get_or_create(name='Clothing', slug='clothing')

    print("Creating products...")
    if not Product.objects.exists():
        Product.objects.create(
            category=electronics,
            name='Smartphone X',
            slug='smartphone-x',
            description='A very cool smartphone with 5G capabilities.',
            price='799.99',
            stock=15
        )
        Product.objects.create(
            category=electronics,
            name='Wireless Headphones',
            slug='wireless-headphones',
            description='Noise cancelling over-ear headphones.',
            price='199.50',
            stock=30
        )
        Product.objects.create(
            category=clothing,
            name='Cotton T-Shirt',
            slug='cotton-t-shirt',
            description='100% cotton casual t-shirt.',
            price='19.99',
            stock=100
        )
        Product.objects.create(
            category=clothing,
            name='Denim Jeans',
            slug='denim-jeans',
            description='Classic blue denim jeans.',
            price='49.99',
            stock=50
        )

    print("Seed data loaded successfully!")

if __name__ == '__main__':
    seed_data()

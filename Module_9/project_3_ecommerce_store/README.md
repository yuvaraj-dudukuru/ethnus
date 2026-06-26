# 🛒 Project 3 — E-Commerce Store (ShopCart)

A full-stack **Django + DRF** shop: product catalog, a per-user cart, and a
**transactional checkout** that snapshots prices and decrements stock atomically.

## What it does
- **Catalog**: products with categories, images, price, stock; search + price/category
  filter; **cursor pagination** (scales to large catalogs).
- **Cart**: AJAX add/remove, live cart badge — private to each logged-in user.
- **Checkout**: `transaction.atomic()` — creates the order, writes a
  `price_at_purchase` **snapshot** per line, decrements stock with `F()`, empties cart.
- **Orders**: read-only history, **owner-scoped (IDOR-safe)** — you only see yours.
- **Auth**: customers shop; only admins create/edit products.

## Run locally
```powershell
python -m venv venv; venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed        # admin/admin + shopper1/shopper + products
python manage.py runserver
```
**/** storefront · **/admin/** (admin/admin) · **/api/** · **/api/docs/**.

## Key endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/products/?search=&category=&max_price=` | catalog (public, cursor-paged) |
| GET/POST | `/api/cart/`, `/api/cart/add/`, `/api/cart/remove/` | cart (login) |
| POST | `/api/cart/checkout/` | transactional order |
| GET | `/api/orders/` | own orders only |

## Testing
```powershell
python manage.py test
```
Covers: public catalog, add-to-cart needs login, **checkout empties cart + decrements
stock**, **price snapshot survives a later price change**, empty-cart checkout → 400,
and **owner-scoped orders**.

## Future scope
Payment gateway (Stripe/Razorpay), reviews, wishlists, recommendations.

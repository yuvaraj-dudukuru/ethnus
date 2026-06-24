# Project 4 — E-Commerce Mini Store 🛒

A small but complete **Django** online store: browse products by category, add
them to a **session-based shopping cart**, register/log in, **check out** to turn
the cart into a permanent order, and review past orders. It is Module 4's best
example of the **session framework**, **`DecimalField` money handling**,
**price snapshotting**, **context processors** and **image uploads**.

> **Part of:** Module 4 — Django Web Applications (Project 4 of 5)

---

## 1. What it does (Overview)

| Feature | Description |
|---------|-------------|
| **Product catalog** | Products grouped into categories, each with price, stock and image. |
| **Category filter** | Click a category to see only its products. |
| **Shopping cart** | Stored in the **session** (no DB row until checkout) — fast and simple. |
| **Cart badge** | A context processor injects the live item count into every page. |
| **Register / Login / Logout** | Full account flow using Django's auth forms. |
| **Checkout** | Converts the cart into an `Order` + `OrderItem` rows (login required). |
| **Price snapshot** | Each `OrderItem` stores the price *at purchase time* for history accuracy. |
| **My Orders** | Logged-in users see their own order history. |

---

## 2. Login credentials (IMPORTANT)

| Field | Value |
|-------|-------|
| **Username** | `admin` |
| **Password** | `admin` |
| **Admin panel** | http://127.0.0.1:8000/admin/ |
| **Store login** | http://127.0.0.1:8000/login/ |

> 🔑 You can shop and fill a cart **without** logging in, but you must be logged in
> to **check out**. Use `admin` / `admin`, or **register your own account** at
> http://127.0.0.1:8000/register/ (you are logged in automatically after signup).
> These weak credentials are for learning only.

---

## 3. Technology stack

- **Python 3.13** (any 3.12+ works)
- **Django 6.0** — web framework
- **Pillow** — required for product image uploads (`ImageField`)
- **SQLite** — file database (`db.sqlite3`)
- **Bootstrap 5** (CDN) — responsive product grid

---

## 4. Project structure

```
project_4_E_commerce_mini_store/
├── manage.py                       # Django command-line entry point
├── seed.py                         # Creates admin + categories + sample products
├── db.sqlite3                      # SQLite database
├── ecommerce/                      # The Django PROJECT (global config)
│   ├── settings.py                 #   Settings; registers cart_count processor; MEDIA
│   ├── urls.py                     #   Includes store urls; serves /media/ in DEBUG
│   └── wsgi.py / asgi.py
├── store/                          # The APP (all store logic)
│   ├── models.py                   #   Category, Product, Order, OrderItem
│   ├── views.py                    #   Catalog, cart, checkout, orders, auth views
│   ├── urls.py                     #   All store routes
│   ├── admin.py                    #   Inline order items, editable price/stock
│   ├── context_processors.py       #   cart_count -> navbar badge on every page
│   └── templates/store/            #   product_list, product_detail, cart, checkout...
└── media/                          # Uploaded product images (created at runtime)
```

### Data model & relationships
```
Category (1) ──< (many) Product
User     (1) ──< (many) Order (1) ──< (many) OrderItem >── (1) Product
```
- **Money** uses `DecimalField` (never `float`) to avoid rounding errors.
- **`OrderItem.price_at_purchase`** is a *snapshot* of the product price at checkout
  time, so editing a product's price later never changes old orders.
- The **cart** is just a dictionary in `request.session` mapping
  `"product_id" -> quantity`.

---

## 5. How to run it (step by step)

> The bundled `venv/` was built on another machine — create a fresh one in step 2.

```powershell
# 1. Open a terminal in this folder (the one with manage.py)

# 2. Create a virtual environment and install Django + Pillow
python -m venv venv
venv\Scripts\activate          # Windows  (macOS/Linux: source venv/bin/activate)
pip install "Django>=6.0,<6.1" Pillow

# 3. Apply database migrations
python manage.py migrate

# 4. Seed the admin account + sample products
python seed.py

# 5. Start the server
python manage.py runserver
```

Then open:
- Storefront (home): **http://127.0.0.1:8000/**
- Admin panel: **http://127.0.0.1:8000/admin/**  (login `admin` / `admin`)

---

## 6. How to test it

This project's `tests.py` is an empty stub, so `manage.py test` finds 0 tests.
Instead, verify everything with Django's **system check** and a manual run:

```powershell
python manage.py check
python manage.py runserver
```

Manual smoke test (matches what was verified during development — all pass):
1. Open `/` → products are listed.
2. Open a product → its detail page loads.
3. Click **Add to cart** → the navbar badge increases and the cart shows the item.
4. Open `/checkout/` while logged out → you are redirected to **login**.
5. Log in as `admin` / `admin`, add an item, **check out** → an order is created
   and you land on the confirmation page; it then appears under **My Orders**.

---

## 7. URL / route reference

| URL | View | Login? | Purpose |
|-----|------|--------|---------|
| `/` | `product_list` | No | All available products |
| `/category/<slug>/` | `product_list` | No | Products in one category |
| `/product/<id>/<slug>/` | `product_detail` | No | One product's page |
| `/cart/` | `cart_view` | No | View the cart |
| `/cart/add/<pid>/` | `cart_add` | No | Add a product to the cart |
| `/checkout/` | `checkout` | **Yes** | Place the order |
| `/order/<pk>/done/` | `order_done` | **Yes** | Order confirmation |
| `/my-orders/` | `MyOrdersView` | **Yes** | Your order history |
| `/register/` `/login/` `/logout/` | auth views | — | Account flow |
| `/admin/` | Django Admin | **Yes (admin)** | Manage products/orders/stock |

---

## 8. Things to try (student exercises)

1. **Stock deduction:** in `checkout`, subtract `qty` from `Product.stock` and
   block adding out-of-stock items to the cart.
2. **Cart controls:** add `+` / `-` / remove buttons on the cart page.
3. **Search:** add a search box that filters products by name/description.
4. **Order status:** in `/admin/`, change an order from *Pending* to *Shipped* and
   watch it update on the My Orders page.

---

## 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'django'` | Activate the venv and install deps (step 2). |
| `cannot import name '_imaging' from 'PIL'` | Reinstall Pillow: `pip install --force-reinstall Pillow`. |
| Product images don't show | Images are optional; upload one in `/admin/` (served from `/media/` in DEBUG). |
| Checkout sends me to login | Expected — log in (or register) first, then check out. |
| Can't log in with `admin` / `admin` | Run `python seed.py` once. |
| Port 8000 in use | `python manage.py runserver 8001`. |

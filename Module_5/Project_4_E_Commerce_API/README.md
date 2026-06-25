# 🛒 Project 4 — E-Commerce REST API (ShopHub)

A small, **fully working** REST API built with **Django** and **Django REST
Framework (DRF)**. It powers an online shop: a public **product catalog**, a
per-user **shopping cart**, and **checkout** that turns the cart into an
**order**. It adds four new skills on top of Projects 1–3:

- **The cart as an API resource** — because token auth is *stateless* (no
  server session to stash a cart in), the cart becomes real database rows
  keyed to the user. This is how real shops work.
- **Checkout as a transactional serializer** — building an order is
  all-or-nothing, so totals are always correct.
- **A price snapshot** — each order line freezes the price paid, so changing a
  product's price later never rewrites history.
- **Owner-scoped data** — you can only ever see your **own** cart and orders
  (the "IDOR-proof" pattern), and the catalog uses **CursorPagination**.

Every code file is heavily commented. Clone it, run it in a few minutes, and
experiment.

---

## 📑 Table of Contents
1. [What is this project?](#-1-what-is-this-project)
2. [What can it do? (the API contract)](#-2-what-can-it-do-the-api-contract)
3. [Logins & passwords (everything you need)](#-3-logins--passwords-everything-you-need)
4. [How to run it (step by step)](#-4-how-to-run-it-step-by-step)
5. [How to use it (try the API)](#-5-how-to-use-it-try-the-api)
6. [How to stop it](#-6-how-to-stop-it)
7. [Running the tests](#-7-running-the-tests)
8. [Project structure (what each file is)](#-8-project-structure-what-each-file-is)
9. [Troubleshooting](#-9-troubleshooting)

---

## 📖 1. What is this project?

It is a **JSON REST API** — a backend other apps talk to over the web.

The data design (extended from Module-4 Project 4) is:

```
Category 1 ───< N Product
User 1 ──(one-to-one)── Cart 1 ───< N CartItem >─── N 1 Product
User 1 ───< N Order 1 ───< N OrderItem >─── N 1 Product
```

**Why is there a Cart model now?** In Module 4 the cart lived in the browser
**session**. But this API authenticates with **tokens**, which are
**stateless** — there is no session "bag" to keep a cart in between requests.
So the cart has to become real rows in the database, attached to the user. Each
user has exactly one cart (a one-to-one link). *(This is a great point to
mention in a viva — it's how real online stores actually do it.)*

**Money is exact.** All prices use `DecimalField`, never floats, so totals add
up to the exact paisa.

---

## 🔌 2. What can it do? (the API contract)

Base address when running locally: `http://127.0.0.1:8000`

| Method | URL | What it does | Who is allowed |
|--------|-----|--------------|----------------|
| POST | `/api/login/` | Send username + password, get a token | Anyone |
| POST | `/api/logout/` | Delete your token (log out) | Logged-in users |
| GET | `/api/products/` | Browse the catalog (cursor-paginated) | **Anyone** |
| POST | `/api/products/` | Add a product | Admin/staff only |
| GET | `/api/products/{id}/` | View one product | Anyone |
| PUT/PATCH/DELETE | `/api/products/{id}/` | Edit/remove a product | Admin/staff only |
| GET | `/api/cart/` | View **my** cart | Logged-in users |
| DELETE | `/api/cart/` | Empty **my** cart | Logged-in users |
| POST | `/api/cart/items/` | Add/update a line `{product, qty}` | Logged-in users |
| DELETE | `/api/cart/items/` | Remove a line `{product}` | Logged-in users |
| GET | `/api/orders/` | List **my** orders | Logged-in users |
| POST | `/api/orders/` | **CHECKOUT** — make an order from my cart | Logged-in users |
| GET | `/api/orders/{id}/` | View one of **my** orders | Owner only |

**Useful query options on `GET /api/products/`:**

| Example | Meaning |
|---------|---------|
| `?category=1` | Only products in category #1 |
| `?min_price=100` | Price 100 or more |
| `?max_price=500` | Price 500 or less |
| `?search=phone` | Find by name or description |
| `?ordering=price` | Sort by price (`-price` for high-to-low) |
| `?cursor=...` | The catalog returns `next`/`previous` cursor links — just follow them |

**Things worth understanding:**
- **Cursor pagination.** The catalog gives you `next` / `previous` links
  instead of page numbers. This stays correct even while products are being
  added or removed — perfect for a big, live shop.
- **Owner-scoped.** `/api/cart/` and `/api/orders/` are always filtered to the
  logged-in user. Even if you guess another user's order id, you get a **404**,
  never their data.
- **Checkout is transactional.** It either fully succeeds (order created, cart
  emptied) or fully fails with nothing left half-done.
- **Price snapshot.** Each order line stores `price_at_purchase`. If the shop
  changes the product price tomorrow, your past order is unchanged.

---

## 🔑 3. Logins & passwords (everything you need)

This is a learning project, so all credentials are simple and listed openly.

| Account | Username | Password | What it's for |
|---------|----------|----------|----------------|
| **Admin** | `admin` | `admin` | Full power: admin panel, add/edit products |
| **Shopper** | `shopper` | `shopper` | A normal customer — use this to fill a cart and check out |

- Both accounts are created automatically by `python manage.py seed`
  (see step 4). You don't type anything.
- Django **admin panel**: `http://127.0.0.1:8000/admin/` — log in with
  **admin / admin**.
- The database is **SQLite** (`db.sqlite3`): a single file, **no separate
  database password or server**.
- The `SECRET_KEY` in `settings.py` is a deliberately fake learning key.

> ⚠️ These weak passwords are fine **only** because this is a practice project.
> Never use them on a real, public server.

---

## ▶️ 4. How to run it (step by step)

You need **Python 3.10 or newer**. Check with `python --version`.

Open a terminal **inside this `Project 4` folder**.

### Windows (PowerShell)

```powershell
python -m venv venv                 # 1) make an isolated environment
venv\Scripts\Activate.ps1           # 2) activate it (prompt shows "(venv)")
#check requirements.txt             # 3) install the packages
python manage.py makemigrations     # 4) prepare the database tables
python manage.py migrate            # 5) build the database
python manage.py seed               # 6) create accounts + sample data
python manage.py runserver          # 7) start the server
```

### macOS / Linux (bash)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed
python manage.py runserver
```

When you see `Starting development server at http://127.0.0.1:8000/`, the API
is **live**. 🎉

> Next time, you only need to **activate the venv** (step 2) and **run the
> server** (step 7) again.

---

## 🧪 5. How to use it (try the API)

### Option A — In your browser (easiest)
- **API home:** http://127.0.0.1:8000/api/
- **Catalog:** http://127.0.0.1:8000/api/products/
- **Cheap electronics:** http://127.0.0.1:8000/api/products/?category=1&max_price=100
- **Interactive docs (Swagger):** http://127.0.0.1:8000/api/docs/
- **Admin panel:** http://127.0.0.1:8000/admin/ (admin / admin)

### Option B — Shop end-to-end (browse → cart → checkout)

**1) Log in as the shopper to get a token:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ -d "username=shopper&password=shopper"
```
Response: `{"token": "abcd1234..."}`

**2) Add 2 of product #1 to the cart** (replace `<TOKEN>`):
```bash
curl -X POST http://127.0.0.1:8000/api/cart/items/ ^
  -H "Authorization: Token <TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"product\": 1, \"qty\": 2}"
```

**3) View the cart (with line totals and a grand total):**
```bash
curl http://127.0.0.1:8000/api/cart/ -H "Authorization: Token <TOKEN>"
```

**4) Check out — this creates the order and empties the cart:**
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ -H "Authorization: Token <TOKEN>"
```

**5) See your orders:**
```bash
curl http://127.0.0.1:8000/api/orders/ -H "Authorization: Token <TOKEN>"
```

*(Windows PowerShell uses `^` to continue lines; macOS/Linux use `\`.)*

### Option C — Postman
Make a collection "Shop API" with an environment holding
`{{base_url}} = http://127.0.0.1:8000` and `{{token}}`, then add one request
per row of the table in section 2.

---

## ⏹️ 6. How to stop it

- **Stop the server:** click the terminal where it's running and press
  **`Ctrl` + `C`**.
- **Leave the virtual environment:** type `deactivate` and press Enter.

Nothing is left running in the background.

---

## ✅ 7. Running the tests

```bash
python manage.py test
```
You should see `OK`. The tests prove:
1. **Checkout** creates an order with the right total and **empties the cart**.
2. The **price snapshot survives a later price change**.
3. Checking out with an **empty cart** is rejected (400).

They use a temporary throwaway database, so your real data is never touched.

---

## 📂 8. Project structure (what each file is)

```
Project 4/
├── manage.py                 # Command tool: runserver, migrate, seed, test...
├── requirements.txt          # The packages to pip install
├── README.md                 # This file
├── .gitignore                # Files Git should not upload
├── db.sqlite3                # The database file (created by "migrate")
│
├── shophub/                  # The PROJECT settings package
│   ├── settings.py           # Master config (apps, database, REST_FRAMEWORK)
│   ├── urls.py               # Master URL address book (router + cart routes)
│   ├── pagination.py         # Default page-number paging (orders etc.)
│   ├── wsgi.py / asgi.py     # Entry points for real servers (untouched)
│   └── __init__.py
│
└── shop/                     # The APP that holds all our logic
    ├── models.py             # Category, Product, Cart, CartItem, Order, OrderItem
    ├── serializers.py        # Product/Cart/Order + the transactional checkout
    ├── filters.py            # ?category=&min_price=&max_price= filters
    ├── pagination.py         # CursorPagination for the product catalog
    ├── permissions.py        # IsAdminOrReadOnly (public read, admin write)
    ├── api_views.py          # Catalog, cart views, owner-scoped orders + checkout
    ├── admin.py              # Registers models in the /admin/ panel
    ├── tests.py              # Checkout + price-snapshot tests
    ├── views.py              # (empty — all logic is in api_views.py)
    ├── apps.py / __init__.py # App plumbing
    ├── migrations/           # Auto-generated database change history
    └── management/commands/
        └── seed.py           # "python manage.py seed" -> accounts + sample data
```

### Where each new "muscle" lives
- **Cart as rows (not sessions)** → `Cart`/`CartItem` in `models.py`,
  `CartView`/`CartItemsView` in `api_views.py`.
- **Transactional checkout** → `OrderCreateSerializer` in `serializers.py`
  (wrapped in `transaction.atomic()`).
- **Price snapshot** → `OrderItem.price_at_purchase` in `models.py`, set during
  checkout.
- **Owner-scoped (IDOR-proof) data** → `get_queryset()` filtering by
  `request.user` in `OrderViewSet`, and per-user cart lookups.
- **CursorPagination** → `shop/pagination.py`, used by `ProductViewSet`.

---

## 🛠️ 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `python: command not found` | Try `python3` instead of `python`. |
| `Activate.ps1 cannot be loaded` (PowerShell) | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again. |
| `No module named django` | The virtual environment isn't active, or you skipped `pip install -r requirements.txt`. |
| `That port is already in use` | Run on another port: `python manage.py runserver 8001`. |
| Login returns `Unable to log in` | Make sure you ran `python manage.py seed`. |
| Checkout returns `400 Cart is empty` | Add something to the cart first via `POST /api/cart/items/`. |
| `403 Forbidden` adding a product | Only admin/staff can add products — log in as `admin`. |
| The catalog has no `?page=` | Correct — it uses cursor paging. Follow the `next`/`previous` links. |
| Want to start completely fresh | Delete `db.sqlite3`, then run `migrate` and `seed` again. |

---

Happy coding! Read the comments inside each file — they explain everything. 🚀

# 📦 Project 4 — Inventory Management Dashboard (Module 6)

A small, **fully working web dashboard** for watching and managing shop stock in
**real-time-ish**. It is the **front-end** built on top of the REST API from
Module 5. The page never reloads — it quietly re-asks the server for the latest
stock every few seconds and updates the table in place (**AJAX + polling**).

> **In one sentence:** Module 5 built the *engine* (a JSON API); Module 6 builds
> a *live dashboard* that keeps itself up to date.

**⭐ The star feature** is **live polling + diffing**: every 10 seconds the page
re-fetches the products and compares the new numbers to what's on screen. Stock
cells that **changed flash** (green = up, red = down), and **low-stock rows
auto-highlight**.

Every file is **heavily commented** so you can read it and understand exactly
what each line does. Clone it, run it in a few minutes, and experiment.

---

## 📑 Table of Contents
1. [What is this project?](#-1-what-is-this-project)
2. [What can it do? (features)](#-2-what-can-it-do-features)
3. [Logins & passwords (everything you need)](#-3-logins--passwords-everything-you-need)
4. [Requirements](#-4-requirements)
5. [How to run it (step by step)](#-5-how-to-run-it-step-by-step)
6. [How to use the dashboard](#-6-how-to-use-the-dashboard)
7. [See the live updates yourself](#-7-see-the-live-updates-yourself)
8. [How to stop it](#-8-how-to-stop-it)
9. [How it works (polling, diffing, WebSockets)](#-9-how-it-works-polling-diffing-websockets)
10. [Project structure (what each file is)](#-10-project-structure-what-each-file-is)
11. [Troubleshooting](#-11-troubleshooting)

---

## 📖 1. What is this project?

It is a **single-page dashboard** that runs in your web browser. It shows a live
table of products and their stock, and lets an admin manage the catalog:

- **Watch stock** update automatically every 10 seconds.
- **See changes flash** the moment a number goes up or down.
- **Spot low stock** instantly (those rows highlight themselves).
- **Add / Edit / Delete** products (admin only) — full CRUD, like Project 1.
- **Search** products by name.

The page itself ([shop/templates/shop/dashboard.html](shop/templates/shop/dashboard.html))
is almost empty — it only draws the frame (toolbar, empty table, the add/edit
pop-up). All the real action lives in one JavaScript file
([static/js/dashboard.js](static/js/dashboard.js)).

---

## ✨ 2. What can it do? (features)

| Feature | What you do | What happens behind the scenes |
|---|---|---|
| **Live stock** | Just watch | Every 10s: `GET /api/products/` → table is diffed & updated |
| **Flash on change** ⭐ | (automatic) | A changed stock cell animates green (up) or red (down) |
| **Low-stock highlight** | (automatic) | Rows with stock ≤ 25 turn yellow; 0 turns red |
| **Search** | Type in the box | `GET /api/products/?search=phone` (debounced) |
| **Refresh now** | Click ↻ | An immediate `GET` instead of waiting for the timer |
| **Pause/resume** | Toggle "Auto-refresh" | Starts/stops the 10-second timer |
| **Add product** | **+ Add** → fill the form | `POST /api/products/` (admin only) |
| **Edit product** | **Edit** → change → Save | `PATCH /api/products/<id>/` (admin only) |
| **Delete product** | **Delete** → confirm | `DELETE /api/products/<id>/` (admin only) |

**Viewing stock is public.** Adding/editing/deleting requires an **admin login**.

---

## 🔑 3. Logins & passwords (everything you need)

This is a **learning project**, so the passwords are deliberately simple and are
listed here on purpose. **Never use passwords like these on a real website.**

| Who | Username | Password | What it can do |
|---|---|---|---|
| **Admin** | `admin` | `admin` | Everything: add / edit / delete products, plus the Django admin panel |
| **Shopper** | `shopper` | `shopper` | A normal (non-staff) user — can log in, but **cannot** change products |

- Both accounts are created automatically by the `seed` command (step 4) — you
  do **not** create them yourself.
- **To manage products, log in as `admin / admin`** in the top bar. (If you log
  in as `shopper`, the Add/Edit/Delete buttons stay hidden, because changing
  products is staff-only.)
- `admin / admin` also works at the Django admin panel:
  <http://127.0.0.1:8000/admin/>.

---

## 🧰 4. Requirements

- **Python 3.10 or newer** (tested on 3.13). Check with `python --version`.
- That's it. Everything else is installed from
  [requirements.txt](requirements.txt) in step 4.
- An internet connection the **first time** you open the page (Bootstrap loads
  from a CDN).

The database is **SQLite** — a tiny file (`db.sqlite3`) created automatically.

---

## ▶️ 5. How to run it (step by step)

Open a terminal **inside the `project_4` folder** and run these in order.
(On **Windows** use the PowerShell lines; on **macOS/Linux** use the others.)

### Step 1 — Create a virtual environment

```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

When it works, your prompt shows `(venv)`.

### Step 2 — Install the libraries

```bash
pip install -r requirements.txt
```

### Step 3 — Create the database tables

```bash
python manage.py migrate
```

### Step 4 — Create the accounts + sample products

```bash
python manage.py seed
```

This creates `admin / admin` and `shopper / shopper`, plus sample categories and
products. Safe to run more than once.

### Step 5 — Start the server

```bash
python manage.py runserver
```

### Step 6 — Open the dashboard

Go to:

> **<http://127.0.0.1:8000/>**

You should see the **Inventory Management Dashboard** with a table of products
and a pulsing green "live" dot. 🎉

---

## 🖱️ 6. How to use the dashboard

1. **Watch the table.** The green dot and "Auto-refresh (10s)" switch mean the
   page is polling the server. "Last updated" shows the time of the last fetch.
2. **Log in as admin** to manage products: top bar → `admin` / `admin`.
3. **Add a product:** click **+ Add product**, fill the form (name, category,
   price, stock), Save.
4. **Edit a product:** click **Edit** on a row, change values (e.g. the stock),
   Save. Within 10 seconds (or immediately if you Save), the cell will reflect
   the new number.
5. **Delete a product:** click **Delete** and confirm.
6. **Search:** type a name in the 🔍 box.
7. **Refresh now / pause:** use ↻ to fetch immediately, or untick Auto-refresh
   to stop polling.

Rows with **stock ≤ 25** are flagged **Low** (yellow); **0** shows **Out of
stock** (red). You can change the threshold near the top of
[static/js/dashboard.js](static/js/dashboard.js) (`LOW_STOCK`).

---

## 🔬 7. See the live updates yourself

The flashing only happens when stock actually changes, so here's how to make it
happen and watch it:

1. Open the dashboard in your browser and leave it running.
2. In a **second** browser tab, open the admin panel
   <http://127.0.0.1:8000/admin/> (`admin` / `admin`) → **Products** → open a
   product → change its **stock** → **Save**.
3. Switch back to the dashboard tab. Within 10 seconds that product's stock cell
   will **flash** (green if you raised it, red if you lowered it) and the row
   will gain/lose the **Low** highlight if it crossed the threshold.

(Or just press **F12 → Network**, tick **Fetch/XHR**, and watch the
`products/` request fire every 10 seconds.)

---

## ⏹️ 8. How to stop it

- In the terminal running the server, press **`Ctrl` + `C`**.
- To leave the virtual environment, type `deactivate`.
- Your data stays saved in `db.sqlite3`.

---

## 🔄 9. How it works (polling, diffing, WebSockets)

### Polling (the simple "live" trick)

```js
setInterval(refresh, 10000);   // ask the server again every 10 seconds
```

Every tick, the JavaScript calls `GET /api/products/`. The products API uses
**cursor pagination** (it returns `next`/`previous` links, not page numbers), so
to load the *whole* inventory the code simply **follows the `next` links** until
there are none left.

### Diffing (only change what changed)

The page remembers the stock number it currently shows for each product. When new
data arrives it **compares**:

```
  for each product from the server:
      if it's new            -> add a row
      else if stock changed  -> update the cell AND flash it (up=green, down=red)
  for each row no longer in the data -> remove it (product was deleted)
```

This "diff the displayed values against the fetched values" is the new muscle of
this project. Re-drawing only what changed is what makes the flash meaningful (it
flashes the *one* cell that moved, not the whole table).

### Low-stock highlight

Pure front-end logic with `classList`: if `stock <= LOW_STOCK` the row gets
Bootstrap's `table-warning` class; if `stock === 0` it gets `table-danger`.

### What about *true* real-time? (WebSockets / Django Channels)

Polling is "real-time-ish": the browser keeps **asking**. For **true push** —
where the server **tells** every open dashboard the instant stock changes — you'd
use **WebSockets**, typically via **Django Channels**. That keeps a connection
open both ways, so updates arrive immediately with no repeated requests. It's
more powerful but needs extra setup (an ASGI server, a channel layer). Polling is
the right first step and needs none of that — which is why we use it here.

---

## 🗂️ 10. Project structure (what each file is)

```
project_4/
├── manage.py                        # Django's command tool (runserver, migrate, seed…)
├── requirements.txt                 # Libraries to install
├── db.sqlite3                       # The database file (auto-created; not in Git)
├── README.md                        # This file
│
├── shophub/                         # Project-wide configuration
│   ├── settings.py                  # All settings; M6 adds STATICFILES_DIRS
│   └── urls.py                      # URL map; M6 adds "/" page, /api/me/, /api/categories/
│
├── shop/                            # The shop app
│   ├── models.py                    # Category, Product, Cart, Order…           (M5)
│   ├── serializers.py               # Objects ↔ JSON                            (M5)
│   ├── api_views.py                 # ViewSets; M6 adds CategoryViewSet & MeView
│   ├── filters.py                   # ?category=&min_price= filtering           (M5)
│   ├── pagination.py                # CursorPagination for the catalog          (M5)
│   ├── permissions.py               # IsAdminOrReadOnly (staff writes)          (M5)
│   ├── management/commands/seed.py  # The "python manage.py seed" helper        (M5)
│   └── templates/shop/
│       └── dashboard.html           # ⭐ M6: the page SHELL (HTML frame only)
│
└── static/js/
    └── dashboard.js                 # ⭐ M6: ALL the front-end logic (poll + diff + CRUD)
```

**The two files Module 6 is really about** are marked ⭐. The rest is the
Module-5 API. The M6 backend additions are small and clearly commented:

1. `STATICFILES_DIRS` in `settings.py` (serve the JS).
2. A `/` dashboard route in `urls.py`.
3. A read-only **`CategoryViewSet`** (`/api/categories/`) so the add/edit form's
   category dropdown can be filled — it reuses the existing M5 serializer.
4. A **`/api/me/`** endpoint so the front-end knows whether you're an admin and
   shows the Add/Edit/Delete buttons accordingly.

---

## 🛠️ 11. Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Try `python3`, or install Python 3. |
| Table is empty | Did you run `python manage.py seed`? It creates the sample products. |
| `(venv)` doesn't appear | The activate command didn't run — re-run step 1 for your OS. |
| No Add/Edit/Delete buttons | Log in as `admin / admin` — managing products is staff-only. |
| Nothing ever flashes | Flash only fires when stock *changes*. Change a stock value (see section 7). |
| The live dot isn't pulsing | Auto-refresh is off — tick the "Auto-refresh (10s)" switch. |
| Page looks unstyled | Bootstrap loads from the internet — check your connection. |
| Port 8000 already in use | `python manage.py runserver 8001`, then open <http://127.0.0.1:8001/>. |
| Changed the JS but see no change | Hard-refresh: **Ctrl + F5**. |
| Want a fresh start | Stop the server, delete `db.sqlite3`, run `migrate` and `seed` again. |

---

### 📌 Bonus links (once the server is running)

- **Dashboard:** <http://127.0.0.1:8000/>
- **Interactive API docs (Swagger):** <http://127.0.0.1:8000/api/docs/>
- **Browsable API:** <http://127.0.0.1:8000/api/products/>
- **Who am I?:** <http://127.0.0.1:8000/api/me/>
- **Admin panel:** <http://127.0.0.1:8000/admin/>  (`admin` / `admin`)

Happy learning! 📦

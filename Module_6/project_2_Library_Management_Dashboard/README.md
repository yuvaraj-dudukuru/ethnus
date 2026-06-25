# 📚 Project 2 — Library Management Dashboard (Module 6)

A small, **fully working web dashboard** for running a library. It is the
**front-end** (the part you see and click) built on top of the REST API from
Module 5. Nothing on the page ever reloads — when you filter books, issue a book
or accept a return, JavaScript quietly talks to the API in the background
(**AJAX**) and updates the screen instantly.

> **In one sentence:** Module 5 built the *engine* (a JSON API); Module 6 builds
> the *dashboard* that drives it live in the browser.

**⭐ The star feature** of this project is the **multi-filter bar** over the
books: a search box, an author dropdown and an availability dropdown all combine
into **one** request such as
`GET /api/books/?search=harry&author=2&available=true&page=1`.

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
7. [How to stop it](#-7-how-to-stop-it)
8. [How it works (the multi-filter + actions)](#-8-how-it-works-the-multi-filter--actions)
9. [Project structure (what each file is)](#-9-project-structure-what-each-file-is)
10. [Watch it work: the Network tab](#-10-watch-it-work-the-network-tab)
11. [Troubleshooting](#-11-troubleshooting)

---

## 📖 1. What is this project?

It is a **single-page dashboard** that runs in your web browser. It has three
tabs:

- **📖 Books** — browse and filter every book; **issue** a book to a member.
- **🔄 Loans** — see every borrowing record; **return** a book (staff only).
- **🧑‍🎓 Members** — the list of library members (staff only).

The page itself ([library/templates/library/dashboard.html](library/templates/library/dashboard.html))
is almost empty — it only draws the frame (filter bar, empty tables, buttons,
the issue pop-up). All the real action lives in one JavaScript file
([static/js/dashboard.js](static/js/dashboard.js)), which sends background
requests to the API and fills the page in.

The **API** it talks to is the one from Module 5, reused almost entirely
unchanged (see the small additions in section 9).

---

## ✨ 2. What can it do? (features)

| Feature | What you do | What happens behind the scenes |
|---|---|---|
| **Browse books** | Open the page | `GET /api/books/` → rows are drawn |
| **Multi-filter** ⭐ | Type a search, pick an author, pick availability | All three combine into `GET /api/books/?search=…&author=…&available=…` (debounced) |
| **Pagination** | **Previous / Next** | `GET /api/books/?page=2` |
| **Issue a book** | Click **Issue**, pick member + due date | `POST /api/books/<id>/issue/` → a copy leaves the shelf; the row's badge updates |
| **Return a book** | **Loans** tab → **Return** | `POST /api/issues/<id>/return_book/` → a copy returns; fine stops |
| **View loans** | **Loans** tab | `GET /api/issues/` (staff only) with a Returned / Overdue / On-loan badge |
| **View members** | **Members** tab | `GET /api/members/` (staff only) |
| **Login** | `admin / admin` | `POST /api/login/` returns a token used for staff actions |

**Browsing & filtering books is public.** Issuing, returning, and viewing loans
& members all require a **staff login** (see below).

---

## 🔑 3. Logins & passwords (everything you need)

This is a **learning project**, so the passwords are deliberately simple and are
listed here on purpose. **Never use passwords like these on a real website.**

| Who | Username | Password | What it can do |
|---|---|---|---|
| **Admin** | `admin` | `admin` | Everything: issue & return books, view loans & members, use the Django admin panel |
| **Librarian** | `librarian` | `librarian` | A sample staff member in the "Librarians" group (can add/edit books in the admin/API). *Note: issuing/returning is wired to admin-only, so use **admin** on the dashboard.* |

- Both accounts are created automatically by the `seed` command (step 4) — you
  do **not** create them yourself.
- **To issue/return books or see Loans & Members, log in as `admin / admin`** in
  the top bar of the dashboard.
- The same `admin / admin` works at the Django admin panel:
  <http://127.0.0.1:8000/admin/>.

---

## 🧰 4. Requirements

- **Python 3.10 or newer** (tested on 3.13). Check with `python --version`.
- That's it. Everything else is installed from
  [requirements.txt](requirements.txt) in step 4.
- An internet connection the **first time** you open the page (Bootstrap loads
  from a CDN).

The database is **SQLite** — a tiny file (`db.sqlite3`) created automatically.
No database server, no passwords to configure.

---

## ▶️ 5. How to run it (step by step)

Open a terminal **inside the `project_2` folder** and run these in order.
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

When it works, your prompt shows `(venv)` at the start.

### Step 2 — Install the libraries

```bash
#check requirements.txt
```

### Step 3 — Create the database tables

```bash
python manage.py migrate
```

### Step 4 — Create the accounts + sample books/members

```bash
python manage.py seed
```

This creates `admin / admin` and `librarian / librarian`, plus sample authors,
books and members. Safe to run more than once.

### Step 5 — Start the server

```bash
python manage.py runserver
```

### Step 6 — Open the dashboard

Go to:

> **<http://127.0.0.1:8000/>**

You should see the **Library Management Dashboard** with a list of books. 🎉

---

## 🖱️ 6. How to use the dashboard

1. **Browse books.** The Books tab shows all books with a green **Available** or
   red **Out of stock** badge.
2. **Filter** (the star feature): type in the **Search** box, and/or pick an
   **Author**, and/or pick **Availability**. The table updates automatically,
   combining all three. **Clear** resets them.
3. **Log in** to do staff actions: top bar → `admin` / `admin` → **Login**.
4. **Issue a book:** on an available book, click **Issue**, choose the member and
   a due date in the pop-up, and **Confirm**. The book's available count drops by
   one and its badge updates live.
5. **Return a book:** open the **Loans** tab, find the loan, click **Return**.
   The copy goes back on the shelf and any fine stops growing.
6. **See members:** open the **Members** tab.

Green messages mean success; red messages explain any error (e.g. *"No copies
available."*).

---

## ⏹️ 7. How to stop it

- In the terminal running the server, press **`Ctrl` + `C`**.
- To leave the virtual environment, type `deactivate`.
- Your data stays saved in `db.sqlite3`. Next time, just `activate` and
  `python manage.py runserver` again — no need to migrate or seed twice.

---

## 🔄 8. How it works (the multi-filter + actions)

### The multi-filter (the new muscle)

All three filter inputs write into **one small state object** in the JavaScript:

```js
const filters = { search: '', author: '', available: '', page: 1 };
```

Whenever any input changes, we wait a moment (**debounce**, so we don't fire a
request on every keystroke) and then build **one** URL from that object:

```
  Search "harry"  +  Author "Orwell"  +  Availability "Available"
                       │
                       ▼   (one combined request)
        GET /api/books/?search=harry&author=2&available=true&page=1
```

The server's `BookFilter` (Module 5) understands `author` and `available`, and
DRF's `SearchFilter` understands `search` — so the API does all the work and
returns just the matching page of books.

### The issue / return actions

These use the API's custom **`@action`** endpoints from Module 5:

```
  Issue a book:   POST /api/books/<id>/issue/      { member, due_date }
                  → server checks stock, creates an Issue, copies_available − 1

  Return a book:  POST /api/issues/<id>/return_book/
                  → marks it returned, records today, copies_available + 1
```

After each action the JavaScript re-fetches the affected table so the **status
badge** and stock numbers update on screen — without a page reload.

### Login & tokens

The API lets anyone *read* books, but issuing/returning and viewing loans/members
require staff. When you log in, the page calls `POST /api/login/` and gets a
**token**; the browser attaches it to every staff request as proof of who you
are. Logging out forgets the token.

---

## 🗂️ 9. Project structure (what each file is)

```
project_2/
├── manage.py                        # Django's command tool (runserver, migrate, seed…)
├── requirements.txt                 # Libraries to install
├── db.sqlite3                       # The database file (auto-created; not in Git)
├── README.md                        # This file
│
├── libraryhub/                      # Project-wide configuration
│   ├── settings.py                  # All settings; M6 adds STATICFILES_DIRS
│   ├── urls.py                      # URL map; M6 adds "/" page + /api/authors/
│   └── pagination.py                # "10 books per page" rule
│
├── library/                         # The library app
│   ├── models.py                    # Author, Book, Member, Issue (+ fine logic) (M5)
│   ├── serializers.py               # Objects ↔ JSON, incl. computed fields      (M5)
│   ├── api_views.py                 # ViewSets + issue/return @actions; M6 adds AuthorViewSet
│   ├── filters.py                   # The ?available=&author= FilterSet          (M5)
│   ├── admin.py                     # Registers models in the admin panel        (M5)
│   ├── management/commands/seed.py  # The "python manage.py seed" helper         (M5)
│   └── templates/library/
│       └── dashboard.html           # ⭐ M6: the page SHELL (HTML frame only)
│
└── static/js/
    └── dashboard.js                 # ⭐ M6: ALL the front-end logic (AJAX)
```

**The two files Module 6 is really about** are marked ⭐. Everything else is the
Module-5 API. The **only** backend additions for M6 are small and clearly
commented:

1. `STATICFILES_DIRS` in `settings.py` (so the JS file is served).
2. A `/` dashboard route in `urls.py` (to show the page).
3. A tiny **read-only `AuthorViewSet`** (in `api_views.py`, registered in
   `urls.py`) so the Author filter dropdown can be filled from `/api/authors/`.
   It reuses the `AuthorSerializer` that already existed in Module 5.

---

## 🔬 10. Watch it work: the Network tab

This is the best way to *understand* the project:

1. Open the dashboard.
2. Press **F12** → **Network** tab → tick **Fetch/XHR**.
3. Now use the page. Type in Search, change the Author dropdown, change
   Availability — and watch how they collapse into a **single** request like
   `books/?search=harry&author=2&available=true&page=1`. Click it to see the
   JSON the server sent back.
4. Issue and return a book and watch the `issue/` and `return_book/` requests.

---

## 🛠️ 11. Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Try `python3`, or install Python 3. |
| Books list is empty | Did you run `python manage.py seed`? It creates the sample books. |
| `(venv)` doesn't appear | The activate command didn't run — re-run step 1 for your OS. |
| **Issue / Return** does nothing or says log in | Log in as `admin / admin` in the top bar. |
| Loans / Members tab says 🔒 | Same — those tabs are staff-only; log in first. |
| Member dropdown in the Issue pop-up is empty | It fills after you log in (it needs staff access to read members). |
| "No copies available." | That book has 0 free copies — return one first, or pick another. |
| Page looks unstyled | Bootstrap loads from the internet — check your connection. |
| Port 8000 already in use | `python manage.py runserver 8001`, then open <http://127.0.0.1:8001/>. |
| Changed the JS but see no change | Hard-refresh: **Ctrl + F5**. |
| Want a fresh start | Stop the server, delete `db.sqlite3`, then run `migrate` and `seed` again. |

---

### 📌 Bonus links (once the server is running)

- **Dashboard:** <http://127.0.0.1:8000/>
- **Interactive API docs (Swagger):** <http://127.0.0.1:8000/api/docs/>
- **Browsable API:** <http://127.0.0.1:8000/api/books/>
- **Overdue report (staff):** <http://127.0.0.1:8000/api/reports/overdue/>
- **Admin panel:** <http://127.0.0.1:8000/admin/>  (`admin` / `admin`)

Happy learning! 📚

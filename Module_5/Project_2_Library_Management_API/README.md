# 📚 Project 2 — Library Management REST API (LibraryHub)

A small, **fully working** REST API built with **Django** and **Django REST
Framework (DRF)**. It manages a library: **authors, books, members** and
**issues** (borrowing records). It adds three new skills on top of Project 1:

- **Custom business actions** — borrow a book, return a book.
- **Computed serializer fields** — values calculated on the fly (a book's
  availability, an issue's late **fine**, a book's author name).
- **A computed report** — list of overdue books with the total fine owed.

This project is made for **students learning to build APIs**. Every code file
is heavily commented. Clone it, run it in a few minutes, and experiment.

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

It is a **JSON REST API** — a backend program other apps talk to over the web
using requests (GET, POST…) and get back **JSON**.

The data design (reused unchanged from Module-4 Project 2) is:

```
Author 1 ───< N Book 1 ───< N Issue >─── N 1 Member
```

- An **Author** writes many **Books**.
- A **Book** can be **Issued** (borrowed) many times.
- A **Member** can borrow many books (many **Issues**).
- An **Issue** links one book to one member, with a due date and a fine if late.

**Key idea:** the API just adds a layer on top of these existing models. You
don't rewrite the data — you expose it.

---

## 🔌 2. What can it do? (the API contract)

Base address when running locally: `http://127.0.0.1:8000`

| Method | URL | What it does | Who is allowed |
|--------|-----|--------------|----------------|
| POST | `/api/login/` | Send username + password, get a token | Anyone |
| POST | `/api/logout/` | Delete your token (log out) | Logged-in users |
| GET | `/api/books/` | List books (search/filter/order/pages) | **Anyone** |
| POST | `/api/books/` | Create a book | Librarians / admin |
| GET | `/api/books/{id}/` | Get one book | Anyone |
| PUT/PATCH | `/api/books/{id}/` | Update a book | Librarians / admin |
| DELETE | `/api/books/{id}/` | Delete a book | Librarians / admin |
| **POST** | `/api/books/{id}/issue/` | **Borrow this book** (stock-checked) | Admin/staff |
| GET | `/api/members/` | List/CRUD members | **Staff only** |
| GET | `/api/issues/` | List borrowing records | Staff only |
| GET | `/api/issues/{id}/` | Get one borrowing record | Staff only |
| **POST** | `/api/issues/{id}/return_book/` | **Return a borrowed book** | Admin/staff |
| GET | `/api/reports/overdue/` | Overdue books + fines owed | Staff only |

**Useful query options on `GET /api/books/`:**

| Example | Meaning |
|---------|---------|
| `?available=true` | Only books with a free copy |
| `?author=1` | Only books by author #1 |
| `?search=potter` | Find by title or ISBN |
| `?ordering=title` | Sort by title (`-title` for reverse) |
| `?page=2` | Second page of results |

**How borrowing works (the interesting part):**
- `POST /api/books/{id}/issue/` first checks the book has copies left. If not,
  it returns **400** with `{"detail": "No copies available."}`. Otherwise it
  creates an Issue (you send `member` and `due_date`) and reduces the available
  copies by 1.
- `POST /api/issues/{id}/return_book/` marks the issue returned, records the
  date, and puts the copy back on the shelf (+1).
- The **fine** is calculated automatically: days late × ₹5/day. An on-time
  return has a fine of 0.

---

## 🔑 3. Logins & passwords (everything you need)

This is a learning project, so all credentials are simple and listed openly.

| Account | Username | Password | What it's for |
|---------|----------|----------|----------------|
| **Admin** | `admin` | `admin` | Full power: admin panel, issue/return books, members, reports |
| **Librarian** | `librarian` | `librarian` | In the "Librarians" group — can create/edit/delete **books** (demonstrates group permissions) |

- Both accounts are created automatically by `python manage.py seed`
  (see step 4). You don't type anything.
- Django **admin panel**: `http://127.0.0.1:8000/admin/` — log in with
  **admin / admin**.
- The **"Librarians" group** shows off `DjangoModelPermissions`: a librarian
  isn't a superuser, but because they're in the group they hold the
  `library.add_book` / `change_book` / `delete_book` permissions, so they can
  manage books. (Issuing/returning and reports are kept admin-only in the code.)
- The database is **SQLite** (`db.sqlite3`): a single file, **no separate
  database password or server**.
- The `SECRET_KEY` in `settings.py` is a deliberately fake learning key.

> ⚠️ These weak passwords are fine **only** because this is a practice project.
> Never use them on a real, public server.

---

## ▶️ 4. How to run it (step by step)

You need **Python 3.10 or newer**. Check with `python --version`.

Open a terminal **inside this `Project 2` folder**.

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
- **Books:** http://127.0.0.1:8000/api/books/
- **Available books only:** http://127.0.0.1:8000/api/books/?available=true
- **Interactive docs (Swagger):** http://127.0.0.1:8000/api/docs/
- **Admin panel:** http://127.0.0.1:8000/admin/ (admin / admin)

### Option B — Borrow and return a book (the full flow)

**1) Log in as admin to get a token:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ -d "username=admin&password=admin"
```
Response: `{"token": "abcd1234..."}`

**2) Borrow book #1 for member #1, due in a week** (replace `<TOKEN>`):
```bash
curl -X POST http://127.0.0.1:8000/api/books/1/issue/ ^
  -H "Authorization: Token <TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"member\": 1, \"due_date\": \"2026-07-15\"}"
```
*(Windows PowerShell uses `^` to continue lines; macOS/Linux use `\`.)*

**3) See the borrowing records:**
```bash
curl http://127.0.0.1:8000/api/issues/ -H "Authorization: Token <TOKEN>"
```

**4) Return that issue (say it was issue #1):**
```bash
curl -X POST http://127.0.0.1:8000/api/issues/1/return_book/ -H "Authorization: Token <TOKEN>"
```

**5) Check the overdue report:**
```bash
curl http://127.0.0.1:8000/api/reports/overdue/ -H "Authorization: Token <TOKEN>"
```

> Tip: book "Animal Farm" is seeded with **0 copies available**, so trying to
> issue it returns **400 — No copies available**. Great for testing the stock
> check.

### Option C — Postman
Make a collection "Library API" with an environment holding
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
You should see `OK`. The two tests prove:
1. Issuing a book with **no copies** returns **400** (the stock check).
2. The **overdue report** computes the correct fine and total.

They use a temporary throwaway database, so your real data is never touched.

---

## 📂 8. Project structure (what each file is)

```
Project 2/
├── manage.py                 # Command tool: runserver, migrate, seed, test...
├── requirements.txt          # The packages to pip install
├── README.md                 # This file
├── .gitignore                # Files Git should not upload
├── db.sqlite3                # The database file (created by "migrate")
│
├── libraryhub/               # The PROJECT settings package
│   ├── settings.py           # Master config (apps, database, REST_FRAMEWORK)
│   ├── urls.py               # Master URL address book (router + reports + docs)
│   ├── pagination.py         # 10-items-per-page rule
│   ├── wsgi.py / asgi.py     # Entry points for real servers (untouched)
│   └── __init__.py
│
└── library/                  # The APP that holds all our logic
    ├── models.py             # Author, Book, Member, Issue (+ is_available, fine)
    ├── serializers.py        # JSON shapes + computed fields (book_title, fine…)
    ├── filters.py            # The ?available= and ?author= filters
    ├── api_views.py          # ViewSets, issue/return actions, overdue report
    ├── admin.py              # Registers models in the /admin/ panel
    ├── tests.py              # Stock-check + overdue-math tests
    ├── views.py              # (empty — all logic is in api_views.py)
    ├── apps.py / __init__.py # App plumbing
    ├── migrations/           # Auto-generated database change history
    └── management/commands/
        └── seed.py           # "python manage.py seed" -> accounts + sample data
```

### Where each new "muscle" lives
- **Custom actions** (`issue`, `return_book`) → `api_views.py` (`@action`).
- **Stock check + F() update** of `copies_available` → `api_views.py`.
- **Computed serializer fields** (`book_title`, `member_name`, `fine`,
  `is_available`, `author_name`) → `serializers.py`, backed by the `@property`
  methods in `models.py`.
- **Overdue report with fine math** → `OverdueReport` in `api_views.py`.
- **Group permissions** (Librarians + `DjangoModelPermissions`) → `BookViewSet`
  in `api_views.py` and the `seed.py` command.

---

## 🛠️ 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `python: command not found` | Try `python3` instead of `python`. |
| `Activate.ps1 cannot be loaded` (PowerShell) | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again. |
| `No module named django` | The virtual environment isn't active, or you skipped `pip install -r requirements.txt`. |
| `That port is already in use` | Run on another port: `python manage.py runserver 8001`. |
| Login returns `Unable to log in` | Make sure you ran `python manage.py seed`. |
| Issuing a book returns 400 | That book has 0 copies available — that's the stock check working. Try book #1 or #2. |
| `403 Forbidden` when writing | You're not logged in, or your account lacks permission for that action. |
| Want to start completely fresh | Delete `db.sqlite3`, then run `migrate` and `seed` again. |

---

Happy coding! Read the comments inside each file — they explain everything. 🚀

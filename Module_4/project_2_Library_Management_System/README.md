# Project 2 — Library Management System 📚

A **Django** web application that models the day-to-day operations of a library:
cataloguing books, registering members, issuing/returning books, tracking stock
and calculating overdue fines. It is the strongest example in Module 4 of
**relational database design**, **atomic updates**, **computed properties** and
**automated testing**.

> **Part of:** Module 4 — Django Web Applications (Project 2 of 5)

---

## 1. What it does (Overview)

| Feature | Description |
|---------|-------------|
| **Catalog books** | Each book stores total copies and available copies. |
| **Register members** | Library users with a unique email and join date. |
| **Issue a book** | Check a book out to a member (available copies go **down by 1**). |
| **Return a book** | Process a return (available copies go **up by 1**). |
| **Stock protection** | A book with `0` available copies **cannot** be issued. |
| **Overdue report** | Lists every book that is past its due date and not returned. |
| **Fine calculation** | Automatically `$5 per day` overdue, computed on the fly. |

---

## 2. Login credentials (IMPORTANT)

| Field | Value |
|-------|-------|
| **Username** | `admin` |
| **Password** | `admin` |
| **Admin panel** | http://127.0.0.1:8000/admin/ |

> 🔑 Issuing and returning books require you to be **logged in**. The simplest way
> is to log in once at the **admin panel** (`admin` / `admin`); your session then
> works across the whole site. These weak credentials are for learning only.

---

## 3. Technology stack

- **Python 3.13** (any 3.12+ works)
- **Django 6.0** — web framework (no Pillow needed; this project has no images)
- **SQLite** — file database (`db.sqlite3`)

---

## 4. Project structure

```
project_2_Library_Management_System/
├── manage.py                 # Django command-line entry point
├── setup_data.py             # Creates admin user + sample authors/books/members
├── db.sqlite3                # SQLite database
├── lms/                      # The Django PROJECT (global config)
│   ├── settings.py           #   Settings (apps, DB, LOGIN_URL -> admin login)
│   ├── urls.py               #   '/' redirects to /library/books/
│   └── wsgi.py / asgi.py
└── library/                  # The APP (all the library logic)
    ├── models.py             #   Author, Book, Member, Issue tables
    ├── views.py              #   List/Detail views + issue_book/return_book
    ├── forms.py              #   IssueForm (pick member + due date)
    ├── urls.py               #   /books, /members, /issue, /return, /overdue
    ├── admin.py              #   Rich admin (filters, search, date hierarchy)
    ├── tests.py              #   6 automated tests (run with manage.py test)
    └── templates/library/    #   All HTML pages
```

### Data model & relationships
```
Author (1) ──< (many) Book
Book   (1) ──< (many) Issue >── (many) ── (1) Member
```
- **`Book.author`** is a `ForeignKey` with `on_delete=PROTECT` — you cannot delete
  an author who still has books.
- **`Issue`** is the link between a `Book` and a `Member` (who borrowed what).
- **Computed properties** (calculated, *not* stored in the DB):
  - `Book.is_available` → `True` when `copies_available > 0`
  - `Issue.days_overdue` → days past `due_date` (0 if returned/on-time)
  - `Issue.fine` → `days_overdue * 5`
- **Atomic stock updates** use `F()` expressions
  (`copies_available = F('copies_available') - 1`) so two people issuing at the
  same time can never corrupt the count.

---

## 5. How to run it (step by step)

> The bundled `venv/` was built on another machine and won't work here — create a
> fresh one with step 2.

```powershell
# 1. Open a terminal in this folder (the one with manage.py)

# 2. Create a virtual environment and install Django
python -m venv venv
venv\Scripts\activate          # Windows  (use: source venv/bin/activate on macOS/Linux)
pip install "Django>=6.0,<6.1"

# 3. Apply database migrations
python manage.py migrate

# 4. Create the admin account + sample data
python setup_data.py

# 5. Start the server
python manage.py runserver
```

Then open:
- Books list (home): **http://127.0.0.1:8000/**  → redirects to `/library/books/`
- Admin panel: **http://127.0.0.1:8000/admin/**  (login `admin` / `admin`)

---

## 6. How to test it

This project has a **proper Django test suite** (6 tests) covering the business
logic and the views:

```powershell
python manage.py test
```

Expected result:
```
Ran 6 tests in ~4s
OK
```

The tests verify: the `is_available` property, fine calculation, issuing a book
(stock drops), blocking an out-of-stock issue, returning a book (stock rises),
and the overdue report filtering.

---

## 7. URL / route reference

| URL | View | Login? | Purpose |
|-----|------|--------|---------|
| `/` | redirect | No | Sends you to the book list |
| `/library/books/` | `BookListView` | No | List + search (title/author/ISBN) |
| `/library/books/<id>/` | `BookDetailView` | No | One book + its issue history |
| `/library/members/` | `MemberListView` | No | All members |
| `/library/members/<id>/` | `MemberDetailView` | No | Member + borrowed books + total fine |
| `/library/issue/<book_id>/` | `issue_book` | **Yes** | Issue a book to a member |
| `/library/return/<issue_id>/` | `return_book` | **Yes** | Return a borrowed book |
| `/library/overdue/` | `OverdueReportView` | No | Overdue books report |
| `/admin/` | Django Admin | **Yes** | Manage authors/books/members/issues |

---

## 8. Things to try

1. **Issue a book** and watch *available copies* drop by one.
2. Keep issuing until copies reach **0**, then try again → you get
   *“No copies available.”*
3. In the **admin panel**, create an `Issue` with a **due date in the past**, then
   open the **Overdue Report** and a member's page to see the **$5/day fine**.
4. **Return** a book and watch the count go back up.

---

## 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'django'` | Activate the venv and `pip install Django` (step 2). |
| Clicking *Issue/Return* sends you to a login page | That's expected — log in at `/admin/` with `admin` / `admin`, then retry. |
| Login fails with `admin` / `admin` | Run `python setup_data.py` once to create the admin account. |
| Port 8000 in use | `python manage.py runserver 8001`. |

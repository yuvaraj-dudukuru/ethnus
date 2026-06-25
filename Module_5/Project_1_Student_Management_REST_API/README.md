# 🎓 Project 1 — Student Management REST API (CampusHub)

A small, **fully working** REST API built with **Django** and **Django REST
Framework (DRF)**. It manages college **students** and **departments**, with
login tokens, permissions, search/filter/ordering, pagination, rate-limiting
(throttling) and auto-generated interactive documentation.

This project is made for **students learning to build APIs**. Every code file
is heavily commented so you can read it and understand exactly what each line
does. You can clone it, run it in a few minutes, and experiment.

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

It is a **JSON REST API** — a program that other programs talk to over the
internet using simple web requests (GET, POST, etc.) and gets back **JSON**
(structured text) in reply.

This particular API lets you manage two things:

- **Departments** — e.g. "Computer Science" (read-only through the API).
- **Students** — each student belongs to one department (full create / read /
  update / delete).

It is designed to be the backend ("server") for future apps such as a React
website, a mobile app, or partner scripts. Those apps would call this API to
read and change the data.

**Key idea:** the database models are *reused, unchanged* from an earlier
Module 4 project. Module 5 only adds an **API layer** on top of them. That is
the whole point of "layering" — you don't rewrite your data, you expose it.

---

## 🔌 2. What can it do? (the API contract)

This is the full list of endpoints (web addresses) the API answers. The base
address when running locally is `http://127.0.0.1:8000`.

| Method | URL | What it does | Who is allowed |
|--------|-----|--------------|----------------|
| POST   | `/api/login/` | Send username + password, get a token back | Anyone (max 5/min) |
| POST   | `/api/logout/` | Delete your token (log out) | Logged-in users |
| GET    | `/api/departments/` | List all departments | Anyone |
| GET    | `/api/departments/{id}/` | Get one department | Anyone |
| GET    | `/api/students/` | List students (supports search/filter/order/pages) | Anyone |
| POST   | `/api/students/` | Create a new student | Logged-in users |
| GET    | `/api/students/{id}/` | Get one student | Anyone |
| PUT    | `/api/students/{id}/` | Full update of a student | Logged-in users |
| PATCH  | `/api/students/{id}/` | Partial update of a student | Logged-in users |
| DELETE | `/api/students/{id}/` | Delete a student | **Admin only** |
| GET    | `/api/students/toppers/` | The top 5 active students | Anyone |

**Useful query options on `GET /api/students/`:**

| Example | Meaning |
|---------|---------|
| `?search=asha` | Find students whose name/email/department contains "asha" |
| `?department=1` | Only students in department #1 |
| `?is_active=true` | Only active students |
| `?min_marks=80` | Marks 80 or above |
| `?max_marks=90` | Marks 90 or below |
| `?ordering=marks` | Sort by marks ascending (`-marks` for descending) |
| `?page=2` | Show the second page of results |
| `?page_size=25` | Show 25 students per page (max 50) |

**Rule reminder about student emails:** when you create or edit a student, the
email **must end in `@college.edu`** (this rule lives in `serializers.py`).

---

## 🔑 3. Logins & passwords (everything you need)

This is a learning project, so all credentials are simple and listed openly.

| Account | Username | Password | What it's for |
|---------|----------|----------|---------------|
| **Admin** | `admin` | `admin` | Full power: admin panel + can DELETE students |

- The **admin** account is created automatically by the `seed` command
  (see step 5 below) — you do not have to type anything.
- The Django **admin control panel** is at `http://127.0.0.1:8000/admin/`.
  Log in there with **admin / admin**.
- The database is **SQLite**, stored in a single file `db.sqlite3`. It needs
  **no separate database password or server** — that's why it's perfect for
  students.
- The project `SECRET_KEY` (in `settings.py`) is a deliberately fake learning
  key. On a real public website you would replace it and keep it secret.

> ⚠️ These weak passwords are fine **only** because this is a practice project.
> Never use `admin/admin` on a real, public server.

---

## ▶️ 4. How to run it (step by step)

You need **Python 3.10 or newer** installed. Check with `python --version`.

Open a terminal **inside this `Project 1` folder**, then run the commands for
your operating system.

### Windows (PowerShell)

```powershell
# 1) Create a virtual environment (an isolated box for this project's packages)
python -m venv venv

# 2) Activate it (your prompt will show "(venv)")
venv\Scripts\Activate.ps1

# 3) Install all required packages
#check requirements.txt

# 4) Build the database tables from the models
python manage.py makemigrations
python manage.py migrate

# 5) Create the admin/admin user AND load sample data (one command!)
python manage.py seed

# 6) Start the server
python manage.py runserver
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

When you see a line like `Starting development server at http://127.0.0.1:8000/`
the API is **live**. 🎉

> Every time you come back to work on the project later, you only need to
> **activate the venv** (step 2) and **run the server** (step 6) again.

---

## 🧪 5. How to use it (try the API)

### Option A — The easy way: open it in your browser
DRF gives you a clickable "browsable API". Just visit these in any browser:

- **API home:** http://127.0.0.1:8000/api/
- **Students:** http://127.0.0.1:8000/api/students/
- **Top 5:** http://127.0.0.1:8000/api/students/toppers/
- **Interactive docs (Swagger):** http://127.0.0.1:8000/api/docs/
- **Admin panel:** http://127.0.0.1:8000/admin/ (log in with **admin / admin**)

### Option B — Get a login token, then create a student

Most apps prove who they are with a **token**. Here's the full flow.

**1) Log in to get your token** (anyone can call this):

```bash
curl -X POST http://127.0.0.1:8000/api/login/ -d "username=admin&password=admin"
```

You'll get back something like:

```json
{"token": "9a1b2c3d4e5f6071829..."}
```

**2) Use that token to create a student** (writing requires being logged in).
Put the token in an `Authorization` header. Replace `<TOKEN>` with yours:

```bash
curl -X POST http://127.0.0.1:8000/api/students/ ^
  -H "Authorization: Token <TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"roll\": 201, \"name\": \"New Student\", \"email\": \"new@college.edu\", \"marks\": 77, \"department_id\": 1}"
```

*(On Windows PowerShell use `^` to continue lines as shown; on macOS/Linux use
`\` instead.)*

**3) Log out** (deletes your token):

```bash
curl -X POST http://127.0.0.1:8000/api/logout/ -H "Authorization: Token <TOKEN>"
```

### Option C — Postman
Create a collection called **"Student API"** with an environment that has
`{{base_url}} = http://127.0.0.1:8000` and `{{token}} = your token`. Then add
one request per row of the table in section 2. This is exactly the API the
course's Postman lab runs against.

---

## ⏹️ 6. How to stop it

- **Stop the server:** click on the terminal where it is running and press
  **`Ctrl` + `C`**. The server shuts down and the address stops responding.
- **Leave the virtual environment:** type `deactivate` and press Enter. The
  `(venv)` prefix disappears.

That's it — nothing is left running in the background.

---

## ✅ 7. Running the tests

The project includes a couple of automated tests (in `students/tests.py`) that
prove the permissions work. Run them any time with:

```bash
python manage.py test
```

You should see `OK`. The tests use a temporary throwaway database, so they
never touch your real data.

---

## 📂 8. Project structure (what each file is)

```
Project 1/
├── manage.py                 # Command tool: runserver, migrate, seed, test...
├── requirements.txt          # The list of packages to pip install
├── README.md                 # This file
├── .gitignore                # Files Git should not upload
├── db.sqlite3                # The database file (created by "migrate")
│
├── campushub/                # The PROJECT settings package
│   ├── settings.py           # Master config (apps, database, REST_FRAMEWORK)
│   ├── urls.py               # The master URL address book (router lives here)
│   ├── pagination.py         # 10-items-per-page rule
│   ├── wsgi.py / asgi.py     # Entry points for real servers (untouched)
│   └── __init__.py
│
└── students/                 # The APP that holds all our logic
    ├── models.py             # Database design: Department 1—N Student
    ├── serializers.py        # Turns objects <-> JSON, validates input
    ├── filters.py            # The ?min_marks=&department= filters
    ├── api_views.py          # The ViewSets: list/create/update/delete + toppers
    ├── admin.py              # Registers models in the /admin/ panel
    ├── tests.py              # Automated permission tests
    ├── views.py              # (empty — all logic is in api_views.py)
    ├── apps.py / __init__.py # App plumbing
    ├── migrations/           # Auto-generated database change history
    └── management/commands/
        └── seed.py           # "python manage.py seed" -> admin + sample data
```

### The build order these files follow (the recommended way to read them)
1. DRF + authtoken installed/configured → `settings.py`
2. Serializers → `serializers.py`
3. ViewSets → `api_views.py`
4. Router → `urls.py` (then smoke-test the browsable API)
5. Auth endpoints (login/logout) → `urls.py` + `api_views.py`
6. Permissions (incl. admin-only delete) → `api_views.py`
7. Filters / search / ordering → `filters.py` + `api_views.py`
8. Pagination → `pagination.py`
9. Throttles → `settings.py`
10. Custom action (`toppers`) → `api_views.py`
11. Tests → `tests.py`
12. Swagger docs → `settings.py` + `urls.py`

---

## 🛠️ 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `python: command not found` | Try `python3` instead of `python`. |
| `Activate.ps1 cannot be loaded` (PowerShell) | Run PowerShell as admin once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again. |
| `No module named django` | The virtual environment isn't active, or you skipped `pip install -r requirements.txt`. |
| `That port is already in use` | Run on another port: `python manage.py runserver 8001`. |
| Login returns `Unable to log in` | Make sure you ran `python manage.py seed` to create the admin user. |
| Creating a student fails with an email error | The email must end in `@college.edu`. |
| Want to start completely fresh | Delete `db.sqlite3`, then run `migrate` and `seed` again. |

---

Happy coding! Read the comments inside each file — they explain everything. 🚀

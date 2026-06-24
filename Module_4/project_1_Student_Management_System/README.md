# Project 1 — CampusHub: Student Management System

A full-stack **Django** web application for managing college/university student
records. It demonstrates Django's **Class-Based Views (CBVs)**, **ModelForms**,
**authentication**, **role-based access**, **file uploads** (student photos) and
**search + pagination** — all of the core skills of Module 4.

> **Part of:** Module 4 — Django Web Applications (Project 1 of 5)

---

## 1. What it does (Overview)

CampusHub is a central place where staff can maintain student information,
departments, marks and profile pictures. Access is controlled by **role**:

| Role | Who | What they can do |
|------|-----|------------------|
| **Visitor** (not logged in) | Anyone | View the student list, search by name/email, open a student's detail page. **Read-only.** |
| **Staff** (logged-in user) | A registered account | Everything a visitor can do **plus** Add / Edit / Delete students (full CRUD). |
| **Superuser / Admin** | The `admin` account | Everything above **plus** the Django Admin panel at `/admin/` to manage Departments and all data. |

---

## 2. Login credentials (IMPORTANT — read this)

A ready-to-use administrator account is created by the seed script.

| Field | Value |
|-------|-------|
| **Username** | `admin` |
| **Password** | `admin` |
| **Admin panel** | http://127.0.0.1:8000/admin/ |

> 🔑 **All Module 4 projects use the same simple credentials: `admin` / `admin`.**
> These are intentionally weak because this is a **learning/demo** project. Never
> use passwords like this in a real, public application.

You can also **register your own student/staff account** at
http://127.0.0.1:8000/accounts/register/ and log in with it.

---

## 3. Technology stack

- **Python 3.13** (any 3.12+ works)
- **Django 6.0** — web framework
- **Pillow** — required by Django's `ImageField` for student photo uploads
- **SQLite** — zero-config file database (`db.sqlite3`)
- **Bootstrap 5** (via CDN in `base.html`) — styling

---

## 4. Project structure

```
project_1_Student_Management_System/
├── manage.py                 # Django command-line entry point
├── seed.py                   # Creates the admin user + sample data
├── run_tests.py              # Simple end-to-end test script (no DB reset needed)
├── db.sqlite3                # SQLite database file
├── campushub/                # The Django PROJECT (global config)
│   ├── settings.py           #   All settings (apps, DB, auth, media, static)
│   ├── urls.py               #   Root URL routing -> apps
│   ├── wsgi.py / asgi.py     #   Web-server entry points
├── students/                 # APP 1: core student management
│   ├── models.py             #   Department & Student database tables
│   ├── views.py              #   Class-Based Views (List/Detail/Create/Update/Delete)
│   ├── forms.py              #   StudentForm with custom email validation
│   ├── urls.py               #   /, /<id>/, /add/, /<id>/edit/, /<id>/delete/
│   ├── admin.py              #   Admin-site customisation
│   └── templates/students/   #   index, detail, form, confirm_delete pages
├── accounts/                 # APP 2: authentication (register/login/logout)
│   ├── views.py / forms.py   #   Registration view & form
│   ├── urls.py               #   /accounts/register, /login, /logout
│   └── templates/accounts/   #   register & login pages
├── templates/                # Project-wide templates
│   ├── base.html             #   Master layout (Bootstrap, messages block)
│   └── _navbar.html          #   Navigation bar (changes when logged in)
├── static/css/style.css      # Custom styling
└── media/students/photos/    # Uploaded student photos (created at runtime)
```

### Data model
```
Department (1) ───< (many) Student
   name                roll, name, email, marks, is_active,
                       admitted (auto), photo (image), department (FK)
```
- A `Department` can have many `Student`s (one-to-many `ForeignKey`).
- `email` must end with **`@college.edu`** (custom validation in `forms.py`).
- Students are listed ordered by **marks (highest first)**.

---

## 5. How to run it (step by step)

> The `venv/` folder bundled with this project was created on a different
> computer, so its paths will not work on yours. Create a **fresh** virtual
> environment with the two commands in step 2 — it only takes a few seconds.

### Step 1 — Open a terminal in this folder
Open PowerShell / Command Prompt / Terminal inside
`project_1_Student_Management_System` (the folder that contains `manage.py`).

### Step 2 — Create a virtual environment and install dependencies
```powershell
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install "Django>=6.0,<6.1" Pillow
```

### Step 3 — Apply database migrations
```powershell
python manage.py migrate
```

### Step 4 — Create the admin account + sample data
```powershell
python seed.py
```
This creates the **`admin` / `admin`** superuser and 3 sample departments /
students. It is safe to run more than once.

### Step 5 — Start the server
```powershell
python manage.py runserver
```

### Step 6 — Open it in your browser
- Main app: **http://127.0.0.1:8000/**
- Admin panel: **http://127.0.0.1:8000/admin/**  (login `admin` / `admin`)

Press `Ctrl + C` in the terminal to stop the server.

---

## 6. How to test it

A small end-to-end test script visits every page and checks the status codes
and the login protection:

```powershell
python run_tests.py
```

Expected output (all check-marks, no errors):
```
✓ Index page loaded successfully (Visitor)
✓ Login page loaded successfully
✓ Register page loaded successfully
✓ Student detail page loaded successfully
✓ Edit page properly protected from visitors
✓ Delete page properly protected from visitors
✓ Logged in as Staff/Admin successfully
✓ Add student page loaded successfully for staff
...
All endpoints tested successfully. No errors or crashes found!
```

You can also run Django's own system check:
```powershell
python manage.py check
```

---

## 7. URL / route reference

| URL | View | Login needed? | Purpose |
|-----|------|---------------|---------|
| `/` | `StudentListView` | No | List + search + pagination |
| `/<id>/` | `StudentDetailView` | No | One student's full profile |
| `/add/` | `StudentCreateView` | **Yes** | Add a new student |
| `/<id>/edit/` | `StudentUpdateView` | **Yes** | Edit a student |
| `/<id>/delete/` | `StudentDeleteView` | **Yes** | Delete a student |
| `/accounts/register/` | `register` | No | Create a new account |
| `/accounts/login/` | `LoginView` | No | Log in |
| `/accounts/logout/` | `LogoutView` | — | Log out |
| `/admin/` | Django Admin | **Yes (admin)** | Manage everything |

---

## 8. Things to learn / try next

1. **Read the comments.** Every Python file (`models.py`, `views.py`, `forms.py`,
   `urls.py`, `admin.py`) is commented line-by-line — open them and follow the flow
   from URL → View → Model → Template.
2. **Add a field** to `Student` (e.g. `phone`), then create and apply a migration
   with `python manage.py makemigrations` and `python manage.py migrate`.
3. **Add a new model** such as `Course` and link it to `Student`.
4. **Change the email rule** in `forms.py` to allow a different domain.

---

## 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'django'` | You forgot to activate the venv / install Django (step 2). |
| `cannot import name '_imaging' from 'PIL'` | Reinstall Pillow for your Python: `pip install --force-reinstall Pillow`. |
| `UnicodeEncodeError` when running scripts | Already fixed — the scripts force UTF-8 output. Make sure you are running the current files. |
| Login fails with `admin` / `admin` | Run `python seed.py` once to (re)create the admin account. |
| Port 8000 already in use | Run on another port: `python manage.py runserver 8001`. |

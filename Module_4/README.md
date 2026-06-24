# Module 4 — Django Web Applications 🐍🌐

Welcome to **Module 4**! This module is a hands-on collection of **five complete
Django web applications**. Each project is a self-contained, runnable website that
teaches a different slice of real-world web development — from simple CRUD all the
way up to role-based access control, file uploads and a shopping-cart checkout.

Every Python file is **commented for beginners**, every project has its **own
detailed `README.md`**, and every project ships with **ready-made login accounts**
so you can start clicking around immediately.

> **Audience:** students learning Django. The code favours clarity over cleverness,
> and the passwords are intentionally simple (see the security note at the bottom).

---

## 📚 The five projects at a glance

| # | Project | Folder | What you learn | Headline feature |
|---|---------|--------|----------------|------------------|
| 1 | **Student Management System** (CampusHub) | `project_1_Student_Management_System` | Class-Based Views, ModelForms, auth, image upload, search + pagination | Staff CRUD over students & departments |
| 2 | **Library Management System** | `project_2_Library_Management_System` | Relational design, computed `@property`, atomic `F()` updates, **unit tests** | Issue/return books, overdue fines |
| 3 | **Blog Management System** | `project_3_blog_management_system` | Authorization (author-only edit), slug URLs, `form_valid()`, **12 unit tests** | Drafts/published posts + comments |
| 4 | **E-Commerce Mini Store** | `project_4_E_commerce_mini_store` | Session cart, `DecimalField` money, price snapshots, context processors | Browse → cart → checkout → orders |
| 5 | **Job Portal** | `project_5_job_portal` | Role-based access (`Profile`), file upload + validation, `unique_together` | Recruiter & candidate workflows |

Each project's folder has a **much more detailed `README.md`** — open it for the
full feature list, URL map, data model and exercises.

---

## 🔑 Master credentials (all projects)

> These are **demo credentials for learning only**. They are deliberately weak.

| Project | Admin (Django `/admin/`) | Other demo accounts |
|---------|--------------------------|---------------------|
| 1 — Student Mgmt | `admin` / `admin` | — (register your own staff account) |
| 2 — Library | `admin` / `admin` | — |
| 3 — Blog | `admin` / `admin` | (the `admin` user also authors the sample post) |
| 4 — E-Commerce | `admin` / `admin` | register your own shopper |
| 5 — Job Portal | `admin` / `admin` | `recruiter1` / `recruiter`, `candidate1` / `candidate` |

**Every admin account is `admin` / `admin`.** Other accounts use simple,
memorable passwords too.

---

## 🛠️ Prerequisites (read this once)

You only need **Python 3.12 or newer** installed. Check with:

```powershell
python --version
```

### ⚠️ Important: the bundled `venv/` folders do not work on your machine
Each project ships with a `venv/` folder, but those virtual environments were
created on a **different computer** (they point to a Python path that doesn't
exist here). **Do not use the bundled `venv/`.** Instead, create a fresh virtual
environment per project using the steps below — it takes only a few seconds.

### Python packages used across the module
| Package | Used by | Why |
|---------|---------|-----|
| `Django` (6.0) | all 5 | the web framework |
| `Pillow` | projects 1 & 4 | required for `ImageField` (photos/product images) |
| `django-crispy-forms`, `crispy-bootstrap5`, `django-widget-tweaks` | project 5 | nicer form rendering |

---

## 🚀 Quick start (works for every project)

Open a terminal **inside the project folder you want to run** (the folder that
contains `manage.py`), then:

```powershell
# 1. Create and activate a fresh virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 2. Install that project's dependencies (see the table below)
pip install "Django>=6.0,<6.1" Pillow      # projects 1 & 4
# pip install "Django>=6.0,<6.1"           # projects 2 & 3 (no Pillow needed)
# pip install "Django>=6.0,<6.1" Pillow django-crispy-forms crispy-bootstrap5 django-widget-tweaks   # project 5

# 3. Apply database migrations
python manage.py migrate

# 4. Seed demo data + the admin account (script name differs per project)
python seed.py            # project 1 and project 4
# python setup_data.py    # project 2
# python create_users.py  # project 5
# (project 3 has no seed script — it ships with data already, or use createsuperuser)

# 5. Run the development server
python manage.py runserver
```

Then visit **http://127.0.0.1:8000/** (and **/admin/** for the admin panel).
Press `Ctrl + C` to stop the server.

### Per-project cheat sheet

| Project | Install | Seed script | Start |
|---------|---------|-------------|-------|
| 1 — Student Mgmt | `Django Pillow` | `python seed.py` | `python manage.py runserver` |
| 2 — Library | `Django` | `python setup_data.py` | `python manage.py runserver` |
| 3 — Blog | `Django` | *(none — DB pre-seeded)* | `python manage.py runserver` |
| 4 — E-Commerce | `Django Pillow` | `python seed.py` | `python manage.py runserver` |
| 5 — Job Portal | `Django Pillow django-crispy-forms crispy-bootstrap5 django-widget-tweaks` | `python create_users.py` | `python manage.py runserver` |

---

## ✅ How to test each project

All five projects have been verified to run and pass their checks.

| Project | How to test | Result |
|---------|-------------|--------|
| 1 — Student Mgmt | `python run_tests.py` | End-to-end page + auth checks, all ✓ |
| 2 — Library | `python manage.py test` | **6 unit tests** pass |
| 3 — Blog | `python manage.py test` | **12 unit tests** pass |
| 4 — E-Commerce | `python manage.py check` + manual flow | system check clean; storefront/cart/checkout work |
| 5 — Job Portal | `python manage.py check` + manual flow | system check clean; recruiter/candidate flow works |

> Tip: `python manage.py check` works in **every** project and is the fastest way
> to confirm the app is wired up correctly.

---

## 🧠 Django concepts taught across the module

By working through all five projects you will have practised:

- **Project vs App structure** — one Django *project* (settings/urls) containing
  one or more *apps* (models/views/templates).
- **Models & migrations** — defining database tables in Python and evolving them.
- **Relationships** — `ForeignKey` (one-to-many), `OneToOneField`, and the
  `on_delete` behaviours `CASCADE`, `PROTECT`, `SET_NULL`.
- **Class-Based Views** — `ListView`, `DetailView`, `CreateView`, `UpdateView`,
  `DeleteView` — and **Function-Based Views** for custom logic.
- **Forms & validation** — `ModelForm`, custom `clean_*()` methods, file uploads.
- **Authentication & authorization** — login/register, `LoginRequiredMixin`,
  `UserPassesTestMixin`, the `@login_required` decorator, and role checks.
- **The session framework** — a shopping cart with no database row until checkout.
- **Computed properties & atomic updates** — `@property` and `F()` expressions.
- **The Django admin** — inlines, filters, search, prepopulated slugs, editable
  list columns.
- **Templates** — inheritance with `base.html`, context processors, CSRF.
- **Automated testing** — `TestCase`, the test `Client`, assertions.

---

## 📁 What's inside each project folder

```
project_X_.../
├── manage.py            # run commands: runserver, migrate, test, ...
├── README.md            # the DETAILED guide for this specific project
├── seed.py / setup_data.py / create_users.py   # creates demo data + accounts
├── db.sqlite3           # the SQLite database (already has demo data)
├── <project>/           # global config: settings.py, urls.py, wsgi.py
└── <app>/               # the application: models, views, forms, urls, admin, templates
```

👉 **Always read the project's own `README.md`** for the complete details,
credentials, URL map and student exercises specific to that project.

---

## 🆘 Common troubleshooting

| Problem | Cause & fix |
|---------|-------------|
| `ModuleNotFoundError: No module named 'django'` | You didn't activate the venv / install deps. Redo the Quick Start. |
| `No module named 'crispy_forms'` / `widget_tweaks` | Project 5 needs the extra packages — see its install line. |
| `cannot import name '_imaging' from 'PIL'` | Pillow built for another Python. Run `pip install --force-reinstall Pillow`. |
| The bundled `venv` gives a path error | Expected — it was made on another PC. Create a fresh venv (Quick Start step 1). |
| Login fails with `admin` / `admin` | Re-run that project's seed script (see the cheat sheet). |
| `Port 8000 is already in use` | Run on a different port: `python manage.py runserver 8001`. |
| `UnicodeEncodeError` running a script on Windows | Already fixed — make sure you're running the current files. |

---

## 🔒 Security note (please read)

This module is for **learning**. To keep things friction-free for students:

- All admin logins are **`admin` / `admin`**, and other demo passwords are simple.
- `DEBUG = True` and the `SECRET_KEY` is committed in each `settings.py`.

**Never** do any of this in a real, public application. For production you would
use strong unique passwords, set `DEBUG = False`, keep the `SECRET_KEY` and any
credentials in environment variables, restrict `ALLOWED_HOSTS`, and serve behind
HTTPS. Project 5's README includes a short "deployment preparation" checklist if
you want to explore that next.

---

Happy learning — open any project folder and run it! 🎓

# 🎓 Module 9 — Capstone Collection: Ten Full-Stack Django Projects

Welcome to **Module 9**, the capstone module. It contains **ten complete, runnable
full-stack web applications** — each one a Django **REST API + browser frontend** you
can show in a portfolio. They reuse everything from Modules 4–8: models & migrations,
DRF ViewSets/serializers/routers, role-based permissions, `@action` endpoints,
django-filter, Swagger docs, server-rendered templates with vanilla JS, automated
tests, and a Render deployment kit.

> Every project runs **out of the box on SQLite** and is **deployment-ready** for
> Render/Postgres by setting `DEBUG=False` + `DATABASE_URL` (Module 8 style).

---

## 📦 The ten projects (easy → complex)

| # | Project | Folder | Headline feature | Tests |
|---|---------|--------|------------------|:----:|
| 1 | **Student Management** | [`project_1_student_management_system`](./project_1_student_management_system/) | CRUD, search, enrollments, toppers chart | 7 |
| 2 | **Library Management** | [`project_2_library_management_system`](./project_2_library_management_system/) | Issue/return, atomic stock, overdue fines | 6 |
| 3 | **E-Commerce Store** | [`project_3_ecommerce_store`](./project_3_ecommerce_store/) | Cart + transactional checkout, price snapshots | 6 |
| 4 | **Job Portal** | [`project_4_job_portal`](./project_4_job_portal/) | Role-based access + resume upload | 6 |
| 5 | **Learning Management** | [`project_5_learning_management_system`](./project_5_learning_management_system/) | Enroll + lesson progress % | 5 |
| 6 | **Hospital Management** | [`project_6_hospital_management_system`](./project_6_hospital_management_system/) | Strong RBAC + no double-booking | 6 |
| 7 | **Inventory Management** | [`project_7_inventory_management_system`](./project_7_inventory_management_system/) | Atomic stock movements + low-stock alerts | 6 |
| 8 | **Online Examination** | [`project_8_online_examination_system`](./project_8_online_examination_system/) | Auto-grading + server-enforced timer | 7 |
| 9 | **Blog Platform** | [`project_9_blog_platform`](./project_9_blog_platform/) | Drafts, comments, optimistic likes | 7 |
| 10 | **Event Management** | [`project_10_event_management_system`](./project_10_event_management_system/) | Capacity-limited registration | 6 |

**Total: 62 automated tests, all green.** Each folder has its own detailed `README.md`.

---

## ⚠️ These projects need the DRF stack (unlike the template-only modules)

Modules 4 & 7 run on **plain Django**, which is already installed, so they start with no
setup. **Module 9 also needs Django REST Framework** and friends
(`djangorestframework`, `django-filter`, `drf-spectacular`, plus `whitenoise` for
static files). If those aren't installed you'll see:

```
ModuleNotFoundError: No module named 'rest_framework'
```

That is the **only** thing that stops these from running — the code itself is complete
and tested. Install the dependencies once and every project runs.

> **This machine is already set up** — the required packages have been installed, and
> **each project ships a pre-seeded `db.sqlite3`**, so you can jump straight to
> `python manage.py runserver` inside any project folder.

## 🚀 Run any project (Windows PowerShell)

**Quick start (deps already installed, DB already seeded):**

```powershell
cd project_1_student_management_system   # any project folder
python manage.py runserver               # open http://127.0.0.1:8000/
```

**From scratch on a fresh machine (recommended: isolated virtual environment):**

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed          # creates admin/admin + demo data & accounts
python manage.py runserver
```

Then open:

- **http://127.0.0.1:8000/** — the app's frontend
- **http://127.0.0.1:8000/admin/** — Django admin (`admin` / `admin`)
- **http://127.0.0.1:8000/api/** — the browsable REST API
- **http://127.0.0.1:8000/api/docs/** — interactive Swagger documentation

> macOS/Linux: use `source venv/bin/activate` instead of `venv\Scripts\activate`.

---

## 🔑 Demo accounts

Every project's admin is **`admin` / `admin`**. Projects with multiple roles also seed
role accounts (each project's README lists them), e.g.:

| Project | Extra accounts |
|---------|----------------|
| 4 · Job Portal | `recruiter1`/`recruiter`, `candidate1`/`candidate` |
| 5 · LMS | `instructor1`/`instructor`, `student1`/`student` |
| 6 · Hospital | `doctor1`/`doctor`, `patient1`/`patient`, `reception1`/`reception` |
| 9 · Blog | `author1`/`author`, `reader1`/`reader` |
| 10 · Events | `organizer1`/`organizer`, `attendee1`/`attendee` |

> ⚠️ These are deliberately weak **learning** credentials. Never use them on a real
> public deployment.

---

## 🧪 Test any project

```powershell
python manage.py test          # runs that project's suite
python manage.py check         # fastest "is it wired up correctly?" check
```

---

## 🧰 Shared tech stack

`Django 5.2` · `djangorestframework 3.16` · `django-filter` · `drf-spectacular`
(Swagger) · `gunicorn` + `whitenoise` + `dj-database-url` + `psycopg2-binary`
(deployment) · `Pillow` (image/file projects) · Python **3.12**.

Each project ships the standard structure:

```
project_X_.../
├── manage.py
├── requirements.txt
├── README.md              # the detailed per-project guide
├── build.sh / Procfile / render.yaml / runtime.txt / .env.example   # Render deploy kit
├── <config>/              # settings.py, urls.py, wsgi.py, pagination.py
├── <app>/                 # models, serializers, api_views, filters, tests, admin
│   └── management/commands/seed.py
├── templates/             # base.html + the app's pages
└── static/                # css/style.css + js/<app>.js
```

---

## ☁️ Deploy (Module 8 recap)

Each project is Render-ready:
1. Push the project folder to GitHub.
2. Create a Render **Blueprint** from `render.yaml` (web service + Postgres).
3. Render runs `build.sh` (install → collectstatic → migrate) and starts Gunicorn.
4. Set env vars: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`.

`settings.py` reads everything from the environment, so the *same code* runs locally
on SQLite and live on Postgres.

Happy building — pick one, take it all the way, and put the link on your resume! 🎓

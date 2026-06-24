# Project 5 — Job Portal 💼

A two-sided **Django** job board. **Recruiters** post jobs and review applicants;
**Candidates** search jobs and apply with a PDF resume. It is Module 4's most
advanced project: **role-based access** (a `Profile` extends the `User`),
**file uploads with validation**, **`unique_together` data integrity**, and
third-party UI packages (**crispy-forms**, **widget-tweaks**).

> **Part of:** Module 4 — Django Web Applications (Project 5 of 5)

---

## 1. What it does (Overview)

### Candidate (`role = 'C'`)
- Browse active jobs; **search** by title/company/location and **filter** by type.
- **Apply** to a job by uploading a **PDF resume** (max 2 MB) + optional cover note.
- Track every application's status: **Applied → Shortlisted / Rejected**.
- A candidate can apply to a given job only **once** (enforced by the database).

### Recruiter (`role = 'R'`)
- A personal **dashboard** of the jobs they posted.
- **Create** and **edit** job postings (only their own).
- See **all applicants** for a job and **change their status**.

---

## 2. Login credentials (IMPORTANT)

Three demo accounts are created by `create_users.py`. **All passwords are simple
on purpose** (learning project — never do this in production).

| Account | Username | Password | Role |
|---------|----------|----------|------|
| **Admin** | `admin` | `admin` | Superuser (Django Admin) |
| **Recruiter** | `recruiter1` | `recruiter` | Recruiter (`R`) |
| **Candidate** | `candidate1` | `candidate` | Candidate (`C`) |

| Where | URL |
|-------|-----|
| Admin panel | http://127.0.0.1:8000/admin/ |
| Site login | http://127.0.0.1:8000/login/ |
| Register | http://127.0.0.1:8000/register/ |

> 🔑 Log in as **recruiter1** to post jobs and review applicants; log in as
> **candidate1** to search and apply. You can also register fresh accounts and
> pick a role on the sign-up form.

---

## 3. Technology stack

- **Python 3.13** (any 3.12+ works)
- **Django 6.0** — web framework
- **Pillow** — image handling support
- **django-crispy-forms** + **crispy-bootstrap5** — nicely styled forms
- **django-widget-tweaks** — fine-grained form field rendering in templates
- **SQLite** — file database (`db.sqlite3`)

---

## 4. Project structure

```
project_5_job_portal/
├── manage.py                   # Django command-line entry point
├── create_users.py             # Creates admin + recruiter1 + candidate1 accounts
├── db.sqlite3                  # SQLite database
├── job_portal/                 # The Django PROJECT (global config)
│   ├── settings.py             #   Apps incl. crispy_forms/widget_tweaks; MEDIA; crispy packs
│   ├── urls.py                 #   Includes jobs urls; serves /media/ in DEBUG
│   └── wsgi.py / asgi.py
├── jobs/                       # The APP (all job-portal logic)
│   ├── models.py               #   Profile, Job, Application (+ resume validators)
│   ├── views.py                #   List/Detail/Create/Update + role mixins + apply
│   ├── forms.py                #   UserRegisterForm, JobForm, ApplicationForm
│   ├── urls.py                 #   home, jobs, apply, dashboard, applicants...
│   ├── admin.py                #   Admin with resume links + editable status
│   └── migrations/
├── templates/                  # Project-wide templates
│   ├── base.html
│   ├── jobs/                    #   home, job_list, job_detail, apply_job,
│   │                           #   recruiter_dashboard, job_applicants, ...
│   └── registration/           #   login.html, register.html
├── static/                     # CSS / static assets
└── media/resumes/              # Uploaded PDF resumes (created at runtime)
```

### Data model & relationships
```
User (1) ──(1) Profile          # role: 'R' recruiter or 'C' candidate
User (1) ──< (many) Job          # a recruiter's posted jobs
Job  (1) ──< (many) Application >── (many) ── (1) User   # candidate applications
```
- **`Profile`** is a `OneToOneField` to `User` that adds the **role** — this is the
  classic Django pattern for extending the built-in user.
- **`Application.resume`** is a `FileField` validated to be a **PDF ≤ 2 MB**.
- **`unique_together = ('job', 'candidate')`** stops duplicate applications at the
  database level; the view turns the resulting error into a friendly message.

---

## 5. How to run it (step by step)

> The bundled `venv/` was built on another machine — create a fresh one in step 2.

```powershell
# 1. Open a terminal in this folder (the one with manage.py)

# 2. Create a virtual environment and install ALL dependencies
python -m venv venv
venv\Scripts\activate          # Windows  (macOS/Linux: source venv/bin/activate)
pip install "Django>=6.0,<6.1" Pillow django-crispy-forms crispy-bootstrap5 django-widget-tweaks

# 3. Apply database migrations
python manage.py migrate

# 4. Create the demo accounts (admin / recruiter1 / candidate1)
python create_users.py

# 5. Start the server
python manage.py runserver
```

Then open:
- Home: **http://127.0.0.1:8000/**
- Admin panel: **http://127.0.0.1:8000/admin/**  (login `admin` / `admin`)

> ⚠️ This project needs the **three extra packages** in step 2. If you skip them
> you will get `ModuleNotFoundError: No module named 'crispy_forms'`.

---

## 6. How to test it

`tests.py` is an empty stub, so `manage.py test` finds 0 tests. Verify the app
with the system check plus this manual walkthrough (all of it was verified during
development and passes end-to-end):

```powershell
python manage.py check
python manage.py runserver
```

Manual end-to-end flow:
1. Log in as **recruiter1 / recruiter** → open **Dashboard** → **post a job**.
2. Log out, log in as **candidate1 / candidate** → open **Jobs**, find the job →
   **apply** with any PDF file → it shows under **My Applications** as *Applied*.
3. Log back in as **recruiter1** → open the job's **Applicants** → change the
   status to **Shortlisted** → the candidate sees the new status.

---

## 7. URL / route reference

| URL | View | Access | Purpose |
|-----|------|--------|---------|
| `/` | `home` | Public | Landing page |
| `/jobs/` | `JobListView` | Public | Search + filter active jobs |
| `/job/<pk>/` | `JobDetailView` | Public | One job's details |
| `/register/` | `register` | Public | Sign up (choose role) |
| `/login/` `/logout/` | auth views | — | Log in / out |
| `/job/<pk>/apply/` | `apply_job` | **Candidate** | Apply with a PDF resume |
| `/my-applications/` | `my_applications` | **Candidate** | Your applications + status |
| `/dashboard/` | `recruiter_dashboard` | **Recruiter** | Your posted jobs |
| `/job/new/` | `JobCreateView` | **Recruiter** | Post a new job |
| `/job/<pk>/edit/` | `JobUpdateView` | **Recruiter** | Edit your job |
| `/job/<pk>/applicants/` | `job_applicants` | **Recruiter** | Review + update applicants |
| `/admin/` | Django Admin | **Admin** | Manage everything |

---

## 8. Things to try

1. Register **two** accounts — one Recruiter, one Candidate — and play both sides.
2. Try applying to the **same job twice** as a candidate → you get a friendly
   *“You have already applied for this job.”* message (the `unique_together` rule).
3. Try uploading a **non-PDF** or a file **larger than 2 MB** → the form rejects it.
4. As a recruiter, try opening another recruiter's `/job/<pk>/edit/` URL → you
   can't (the view restricts edits to your own jobs).

---

## 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named 'crispy_forms'` (or `widget_tweaks`) | Install the extra packages in step 2. |
| `No module named 'django'` | Activate the venv first. |
| Can't log in with the demo accounts | Run `python create_users.py` once. |
| "Only candidates can apply" message | You're logged in as a recruiter/admin — log in as `candidate1`. |
| Resume upload rejected | It must be a **PDF** and **under 2 MB**. |
| Port 8000 in use | `python manage.py runserver 8001`. |

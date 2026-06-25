# 💼 Project 5 — Job Portal REST API (JobHub)

A small, **fully working** REST API built with **Django** and **Django REST
Framework (DRF)**. It powers a job board with two kinds of users —
**recruiters** (who post jobs and review applicants) and **candidates** (who
apply with an uploaded resume). It adds four new skills on top of Projects 1–4:

- **Role-based permissions, end-to-end** — recruiter-only and candidate-only
  actions enforced everywhere.
- **File upload through the API** — candidates upload a resume using
  *multipart* form-data (this is the one place you don't send raw JSON).
- **Per-role querysets** — the same `/api/applications/` endpoint shows a
  recruiter their applicants and a candidate their own applications, and never
  leaks one user's data to another.
- **A status-transition action** — a recruiter selects or rejects an applicant.

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

It is a **JSON REST API** (with one **file-upload** endpoint) — a backend that
other apps talk to over the web.

The data design (reused from Module-4 Project 5) is:

```
User 1 ──(one-to-one)── Profile           (Profile holds the user's ROLE)
User(recruiter) 1 ───< N Job
Job 1 ───< N Application >─── N 1 User(candidate)
```

- Every user has a **Profile** with a **role**: **R**ecruiter or **C**andidate.
- A **recruiter** posts **Jobs** and reviews the **Applications** to them.
- A **candidate** **applies** to jobs, uploading a **resume** file.

**Key idea:** which actions you're allowed to take, and which data you can see,
both depend on your **role**. That logic lives in small permission classes and
in role-shaped `get_queryset()` methods.

---

## 🔌 2. What can it do? (the API contract)

Base address when running locally: `http://127.0.0.1:8000`

| Method | URL | What it does | Who is allowed |
|--------|-----|--------------|----------------|
| POST | `/api/register/` | Sign up `{username, password, role}` → token | Anyone |
| POST | `/api/login/` | Log in → token | Anyone |
| POST | `/api/logout/` | Delete your token | Logged-in users |
| GET | `/api/jobs/` | List jobs (`?location=&jtype=&search=`) | **Anyone** |
| POST | `/api/jobs/` | Post a job | **Recruiters only** |
| GET | `/api/jobs/{id}/` | View one job | Anyone |
| PUT/PATCH/DELETE | `/api/jobs/{id}/` | Edit/remove a job | **Owning recruiter** |
| POST | `/api/jobs/{id}/apply/` | Apply with a **resume file** + cover note | **Candidates only** (max 10/day) |
| GET | `/api/applications/` | List applications (role-shaped) | Recruiter: to own jobs • Candidate: own |
| GET | `/api/applications/{id}/` | View one application | Same role rules |
| PATCH | `/api/applications/{id}/set_status/` | Select/Reject `{status: "S" or "R"}` | **Owning recruiter** |

**Useful query options on `GET /api/jobs/`:**

| Example | Meaning |
|---------|---------|
| `?location=remote` | Jobs whose location contains "remote" |
| `?jtype=FT` | Only Full Time jobs (`FT`/`PT`/`CT`/`IN`) |
| `?search=python` | Find by title or description |
| `?ordering=created` | Oldest first (`-created` for newest) |

**Things worth understanding:**
- **Roles are everything.** A candidate posting a job gets **403**; a
  non-recruiter calling `set_status` gets **403**.
- **The apply endpoint takes a FILE.** You must send it as *multipart
  form-data*, not raw JSON. In Postman: **Body → form-data**, add a key
  `resume` whose type is **File**, and a text key `cover_note`.
- **Resumes are validated** — only `.pdf`, `.doc`, `.docx`, max 5 MB.
- **One application per job.** Applying twice returns **400**
  `{"detail": "Already applied."}`.
- **Role-shaped data.** `/api/applications/` returns different rows depending
  on who's asking — and Recruiter B can never see Recruiter A's applicants.

---

## 🔑 3. Logins & passwords (everything you need)

This is a learning project, so all credentials are simple and listed openly.

| Account | Username | Password | Role | What it's for |
|---------|----------|----------|------|----------------|
| **Admin** | `admin` | `admin` | Recruiter + superuser | Admin panel, full access |
| **Recruiter** | `recruiter` | `recruiter` | Recruiter | Post jobs, review/decide applicants |
| **Candidate** | `candidate` | `candidate` | Candidate | Apply to jobs with a resume |

- All three accounts are created automatically by `python manage.py seed`
  (see step 4). You don't type anything.
- You can also **make your own account** at `POST /api/register/` and choose a
  role (`"R"` or `"C"`).
- Django **admin panel**: `http://127.0.0.1:8000/admin/` — log in with
  **admin / admin**.
- The database is **SQLite** (`db.sqlite3`): a single file, **no separate
  database password or server**.
- Uploaded resumes are saved under a local `media/` folder (git-ignored).
- The `SECRET_KEY` in `settings.py` is a deliberately fake learning key.

> ⚠️ These weak passwords are fine **only** because this is a practice project.
> Never use them on a real, public server.

---

## ▶️ 4. How to run it (step by step)

You need **Python 3.10 or newer**. Check with `python --version`.

Open a terminal **inside this `Project 5` folder**.

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
- **Jobs:** http://127.0.0.1:8000/api/jobs/
- **Full-time jobs:** http://127.0.0.1:8000/api/jobs/?jtype=FT
- **Interactive docs (Swagger):** http://127.0.0.1:8000/api/docs/
- **Admin panel:** http://127.0.0.1:8000/admin/ (admin / admin)

### Option B — The recruiter/candidate flow

**1) Log in as the candidate to get a token:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ -d "username=candidate&password=candidate"
```
Response: `{"token": "abcd1234..."}`

**2) Apply to job #1 with a resume file** (this is *multipart*, note `-F`):
```bash
curl -X POST http://127.0.0.1:8000/api/jobs/1/apply/ ^
  -H "Authorization: Token <CANDIDATE_TOKEN>" ^
  -F "resume=@C:/path/to/your/cv.pdf" ^
  -F "cover_note=I would love this role!"
```

**3) Log in as the recruiter and see the applicants:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ -d "username=recruiter&password=recruiter"
curl http://127.0.0.1:8000/api/applications/ -H "Authorization: Token <RECRUITER_TOKEN>"
```

**4) Select the applicant (application #1):**
```bash
curl -X PATCH http://127.0.0.1:8000/api/applications/1/set_status/ ^
  -H "Authorization: Token <RECRUITER_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"status\": \"S\"}"
```

*(Windows PowerShell uses `^` to continue lines; macOS/Linux use `\`.)*

### Option C — Postman (best for the file upload) ⭐
This is the recommended way to test the resume upload:
1. Create a collection "Job API" with an environment: `{{base_url}}` and `{{token}}`.
2. For **apply**: choose **POST** `{{base_url}}/api/jobs/1/apply/`, set the
   **Authorization** header to `Token {{token}}`, then go to **Body →
   form-data** and add:
   - key `resume`, change its type dropdown to **File**, pick a PDF;
   - key `cover_note` (type Text) with any message.
3. Send. You'll get **201 Created** back with the application details.

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
1. A **candidate cannot post a job** (403).
2. A **candidate can apply** with an uploaded resume (201).
3. **Applying twice** is rejected (400, "Already applied.").
4. **Recruiter B cannot see Recruiter A's applicants** (role-shaped queryset).

They use a temporary database and a temporary media folder, so your real data
and files are never touched.

---

## 📂 8. Project structure (what each file is)

```
Project 5/
├── manage.py                 # Command tool: runserver, migrate, seed, test...
├── requirements.txt          # The packages to pip install
├── README.md                 # This file
├── .gitignore                # Files Git should not upload
├── db.sqlite3                # The database file (created by "migrate")
├── media/                    # Uploaded resumes land here (created at runtime)
│
├── jobhub/                   # The PROJECT settings package
│   ├── settings.py           # Master config (apps, database, MEDIA, REST_FRAMEWORK)
│   ├── urls.py               # Master URLs (router + register + media serving)
│   ├── pagination.py         # 10-items-per-page rule
│   ├── wsgi.py / asgi.py     # Entry points for real servers (untouched)
│   └── __init__.py
│
└── jobs/                     # The APP that holds all our logic
    ├── models.py             # Profile (role), Job, Application (resume FileField)
    ├── signals.py            # Auto-create a Profile for every new user
    ├── permissions.py        # IsRecruiter, IsCandidate, IsRecruiterOwnerOrReadOnly
    ├── serializers.py        # Register + Job + Application (with file validation)
    ├── filters.py            # ?location=&jtype= filters
    ├── api_views.py          # Register, JobViewSet (+apply), ApplicationViewSet (+set_status)
    ├── admin.py              # Registers models in the /admin/ panel
    ├── tests.py              # Role-permission + role-queryset + upload tests
    ├── apps.py               # Connects the signals on startup
    ├── views.py              # (empty — all logic is in api_views.py)
    ├── migrations/           # Auto-generated database change history
    └── management/commands/
        └── seed.py           # "python manage.py seed" -> accounts + sample jobs
```

### Where each new "muscle" lives
- **Role-based permissions** → `permissions.py` (`IsRecruiter`, `IsCandidate`,
  `IsRecruiterOwnerOrReadOnly`), applied across `api_views.py`.
- **File upload** → `Application.resume` FileField in `models.py`, the
  multipart `apply` action in `api_views.py`, size check in `serializers.py`.
- **Per-role querysets** → `ApplicationViewSet.get_queryset()` in
  `api_views.py`.
- **Status-transition action** → `set_status` in `api_views.py`.
- **Duplicate-apply protection** → `unique_together` in `models.py`, caught and
  turned into a 400 in the `apply` action.

---

## 🛠️ 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `python: command not found` | Try `python3` instead of `python`. |
| `Activate.ps1 cannot be loaded` (PowerShell) | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again. |
| `No module named django` | The virtual environment isn't active, or you skipped `pip install -r requirements.txt`. |
| `That port is already in use` | Run on another port: `python manage.py runserver 8001`. |
| Login returns `Unable to log in` | Make sure you ran `python manage.py seed`. |
| `403` posting a job | Only recruiters can post jobs — log in as `recruiter`. |
| `400` with a file-type error | Resumes must be `.pdf`, `.doc` or `.docx`, max 5 MB. |
| `400 Already applied.` | You already applied to that job; one application per job. |
| Apply fails sending raw JSON | The resume is a file — send the body as **form-data (multipart)**, not JSON. |
| Want to start completely fresh | Delete `db.sqlite3` and the `media/` folder, then run `migrate` and `seed`. |

---

Happy coding! Read the comments inside each file — they explain everything. 🚀

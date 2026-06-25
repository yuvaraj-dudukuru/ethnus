# ✍️ Project 3 — Blog REST API (BlogHub)

A small, **fully working** REST API built with **Django** and **Django REST
Framework (DRF)**. It powers a blog: **posts, categories** and **comments**,
each written by a logged-in user. It adds four new skills on top of Projects
1 & 2:

- **`IsOwnerOrReadOnly`** — anyone can read a post, but only its **author**
  can edit or delete it.
- **Slug lookups** — posts live at clean URLs like `/api/posts/django-tips/`
  instead of `/api/posts/7/`.
- **The two-serializer pattern** — a slim serializer for the list/feed and a
  rich one for the full article.
- **Nested comment routes** — `/api/posts/{slug}/comments/`, with a scoped
  anti-spam throttle.

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

It is a **JSON REST API** — a backend other apps talk to over the web using
requests (GET, POST…) and get back **JSON**.

The data design (reused unchanged from Module-4 Project 3) is:

```
User 1 ───< N Post >─── N 1 Category
User 1 ───< N Comment >─── N 1 Post
```

- A **User** (author) writes many **Posts** and **Comments**.
- A **Post** belongs to one **Category** and has many **Comments**.
- Each post is either a **Draft** (private to its author) or **Published**
  (public). Each post also has a unique **slug** — a clean, URL-friendly
  version of its title, e.g. "Django Tips" → `django-tips`.

**Key idea:** the API just adds a layer on top of these existing models.

---

## 🔌 2. What can it do? (the API contract)

Base address when running locally: `http://127.0.0.1:8000`

| Method | URL | What it does | Who is allowed |
|--------|-----|--------------|----------------|
| POST | `/api/login/` | Send username + password, get a token | Anyone |
| POST | `/api/logout/` | Delete your token (log out) | Logged-in users |
| GET | `/api/posts/` | List **published** posts | **Anyone** |
| POST | `/api/posts/` | Create a post (author auto-stamped) | Logged-in users |
| GET | `/api/posts/{slug}/` | Get one post **by slug** | Anyone |
| PUT/PATCH | `/api/posts/{slug}/` | Edit a post | **Author only** |
| DELETE | `/api/posts/{slug}/` | Delete a post | **Author only** |
| GET | `/api/posts/{slug}/comments/` | List a post's comments | Anyone |
| POST | `/api/posts/{slug}/comments/` | Add a comment (user auto-stamped) | Logged-in users (max 30/hr) |
| GET | `/api/categories/` | List/retrieve categories | Anyone (read-only) |
| GET | `/api/my-posts/` | Your **own** posts, **drafts included** | Logged-in users |

**Useful query options on `GET /api/posts/`:**

| Example | Meaning |
|---------|---------|
| `?search=django` | Find posts by title or body text |
| `?ordering=created` | Oldest first (`-created` for newest first) |
| `?page=2` | Second page of results |

**Things worth understanding:**
- **Drafts are hidden.** The public list only shows Published posts. To see
  your own drafts, log in and call `/api/my-posts/`.
- **Author stamping.** When you create a post or comment, you never send an
  "author" — the server stamps the logged-in user automatically. Nobody can
  post in someone else's name.
- **Owner-only edits.** If you try to PATCH/DELETE a post you didn't write,
  you get **403 Forbidden**.
- **Comment throttle.** The comment endpoint allows at most **30 comments per
  hour** per user, to fight spam.

---

## 🔑 3. Logins & passwords (everything you need)

This is a learning project, so all credentials are simple and listed openly.

| Account | Username | Password | What it's for |
|---------|----------|----------|----------------|
| **Admin** | `admin` | `admin` | Full power: admin panel, can do anything |
| **Writer** | `writer` | `writer` | A normal user; author of the sample posts — great for testing "owner only" rules |

- Both accounts are created automatically by `python manage.py seed`
  (see step 4). You don't type anything.
- Django **admin panel**: `http://127.0.0.1:8000/admin/` — log in with
  **admin / admin**.
- To test the **owner-only** rule, create a second account, log in as it, and
  try to edit one of `writer`'s posts — you'll get **403 Forbidden**.
- The database is **SQLite** (`db.sqlite3`): a single file, **no separate
  database password or server**.
- The `SECRET_KEY` in `settings.py` is a deliberately fake learning key.

> ⚠️ These weak passwords are fine **only** because this is a practice project.
> Never use them on a real, public server.

---

## ▶️ 4. How to run it (step by step)

You need **Python 3.10 or newer**. Check with `python --version`.

Open a terminal **inside this `Project 3` folder**.

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
- **Posts:** http://127.0.0.1:8000/api/posts/
- **One post by slug:** http://127.0.0.1:8000/api/posts/django-tips/
- **Its comments:** http://127.0.0.1:8000/api/posts/django-tips/comments/
- **Interactive docs (Swagger):** http://127.0.0.1:8000/api/docs/
- **Admin panel:** http://127.0.0.1:8000/admin/ (admin / admin)

### Option B — Write a post, comment, and see your drafts

**1) Log in as the writer to get a token:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ -d "username=writer&password=writer"
```
Response: `{"token": "abcd1234..."}`

**2) Create a post** (the author is stamped automatically — replace `<TOKEN>`):
```bash
curl -X POST http://127.0.0.1:8000/api/posts/ ^
  -H "Authorization: Token <TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"My First Post\", \"body\": \"Hello world!\", \"status\": \"P\"}"
```
The response includes the auto-generated `"slug": "my-first-post"`.

**3) Add a comment to it:**
```bash
curl -X POST http://127.0.0.1:8000/api/posts/my-first-post/comments/ ^
  -H "Authorization: Token <TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"body\": \"Nice post!\"}"
```

**4) See your own posts (drafts included):**
```bash
curl http://127.0.0.1:8000/api/my-posts/ -H "Authorization: Token <TOKEN>"
```

*(Windows PowerShell uses `^` to continue lines; macOS/Linux use `\`.)*

> Tip: log in as a **different** user and try to PATCH `writer`'s post — you'll
> get **403 Forbidden**, proving the owner-only rule works.

### Option C — Postman
Make a collection "Blog API" with an environment holding
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
1. A **stranger** trying to PATCH another user's post gets **403**.
2. **Draft** posts are **absent** from the public, anonymous list.

They use a temporary throwaway database, so your real data is never touched.

---

## 📂 8. Project structure (what each file is)

```
Project 3/
├── manage.py                 # Command tool: runserver, migrate, seed, test...
├── requirements.txt          # The packages to pip install
├── README.md                 # This file
├── .gitignore                # Files Git should not upload
├── db.sqlite3                # The database file (created by "migrate")
│
├── bloghub/                  # The PROJECT settings package
│   ├── settings.py           # Master config (apps, database, REST_FRAMEWORK)
│   ├── urls.py               # Master URL address book (router + nested routes)
│   ├── pagination.py         # 10-items-per-page rule
│   ├── wsgi.py / asgi.py     # Entry points for real servers (untouched)
│   └── __init__.py
│
└── blog/                     # The APP that holds all our logic
    ├── models.py             # Category, Post (auto-slug), Comment
    ├── permissions.py        # IsOwnerOrReadOnly (the owner-only rule)
    ├── serializers.py        # Slim list + rich detail serializers, comments
    ├── api_views.py          # PostViewSet, comments route, my-posts, categories
    ├── admin.py              # Registers models in the /admin/ panel
    ├── tests.py              # Owner-403 + drafts-hidden tests
    ├── views.py              # (empty — all logic is in api_views.py)
    ├── apps.py / __init__.py # App plumbing
    ├── migrations/           # Auto-generated database change history
    └── management/commands/
        └── seed.py           # "python manage.py seed" -> accounts + sample data
```

### Where each new "muscle" lives
- **IsOwnerOrReadOnly** → `permissions.py`, applied in `PostViewSet`.
- **Slug lookups** → `lookup_field = 'slug'` in `PostViewSet`; slug auto-built
  in `Post.save()` (`models.py`).
- **Two-serializer pattern** → `get_serializer_class()` in `PostViewSet`,
  using `PostListSerializer` vs `PostSerializer` (`serializers.py`).
- **Nested comments + scoped throttle** → `PostCommentsAPIView` in
  `api_views.py`, with the `'comments': '30/hour'` rate in `settings.py`.
- **Author stamping** → `perform_create()` in `PostViewSet` and the comments
  view.
- **Hidden drafts / my-posts** → `get_queryset()` in `PostViewSet` and
  `MyPostsView`.

---

## 🛠️ 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `python: command not found` | Try `python3` instead of `python`. |
| `Activate.ps1 cannot be loaded` (PowerShell) | Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again. |
| `No module named django` | The virtual environment isn't active, or you skipped `pip install -r requirements.txt`. |
| `That port is already in use` | Run on another port: `python manage.py runserver 8001`. |
| Login returns `Unable to log in` | Make sure you ran `python manage.py seed`. |
| `403 Forbidden` when editing a post | You're not the author — that's the owner-only rule working. |
| A draft isn't in `/api/posts/` | Correct: drafts are hidden. View yours at `/api/my-posts/`. |
| `429 Too Many Requests` on comments | You hit the 30-comments-per-hour anti-spam limit. |
| Want to start completely fresh | Delete `db.sqlite3`, then run `migrate` and `seed` again. |

---

Happy coding! Read the comments inside each file — they explain everything. 🚀

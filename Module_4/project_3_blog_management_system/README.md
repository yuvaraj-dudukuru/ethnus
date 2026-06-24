# Project 3 — Blog Management System ✍️

A **Django** blogging platform where authors write, edit and publish posts,
readers browse by category, and logged-in users leave comments. It is Module 4's
best example of **authorization** (only the author can edit their own post),
**SEO-friendly slug URLs**, **`form_valid()` stamping**, and a 12-test suite.

> **Part of:** Module 4 — Django Web Applications (Project 3 of 5)

---

## 1. What it does (Overview)

| Feature | Description |
|---------|-------------|
| **Write posts** | Create posts as **Draft** (`D`) or **Published** (`P`). |
| **Author-only editing** | A user can edit/update **only the posts they wrote** (others get HTTP 403). |
| **Categories** | Every post belongs to a category; click a category to filter. |
| **Comments** | Logged-in users can comment on published posts. |
| **Dashboard** | Each author sees *their own* posts (drafts + published). |
| **Slug URLs** | Readable URLs like `/post/welcome-to-the-blog/` instead of `/post/1/`. |
| **Admin** | Manage categories, posts and comments; comments edit inline under a post. |

---

## 2. Login credentials (IMPORTANT)

| Field | Value |
|-------|-------|
| **Username** | `admin` |
| **Password** | `admin` |
| **Admin panel** | http://127.0.0.1:8000/admin/ |
| **Site login** | http://127.0.0.1:8000/accounts/login/ |

> 🔑 The `admin` / `admin` account is both the **superuser** (for `/admin/`) and a
> normal **author** (it owns the sample "Welcome to the Blog" post). You can also
> create extra users in the admin panel to test the author-only editing rule.

---

## 3. Technology stack

- **Python 3.13** (any 3.12+ works)
- **Django 6.0** — web framework
- **SQLite** — file database (`db.sqlite3`)
- Django's built-in **auth views** (`django.contrib.auth.urls`) for login/logout

---

## 4. Project structure

```
project_3_blog_management_system/
├── manage.py                 # Django command-line entry point
├── db.sqlite3                # SQLite database (already has admin/admin + 1 post)
├── config/                   # The Django PROJECT (global config)
│   ├── settings.py           #   Settings; LOGIN_REDIRECT_URL = '/'
│   ├── urls.py               #   admin/, blog (''), accounts/ (auth urls)
│   └── wsgi.py / asgi.py
├── blog/                     # The APP (all blogging logic)
│   ├── models.py             #   Category, Post, Comment tables
│   ├── views.py              #   List/Detail/Create/Update + dashboard + add_comment
│   ├── forms.py              #   PostForm, CommentForm
│   ├── urls.py               #   slug-based routes
│   ├── admin.py              #   Inline comments, prepopulated slugs
│   ├── tests.py              #   12 automated tests
│   └── templates/blog/       #   post_list, post_detail, post_form, dashboard, ...
├── templates/registration/
│   └── login.html            #   Login page for the built-in auth views
└── static/css/               # Styling
```

### Data model & relationships
```
User (1) ──< (many) Post >── (many) ── (1) Category
Post (1) ──< (many) Comment >── (many) ── (1) User
```
- `Post.author` → `ForeignKey(User)` with `on_delete=CASCADE` (delete user → delete posts).
- `Post.category` → `ForeignKey(Category)` with `on_delete=SET_NULL` (delete category → post stays, category becomes empty).
- `Post.status` is `'D'` (Draft) or `'P'` (Published); the public list shows **only Published**.
- `Post.get_absolute_url()` returns the slug-based detail URL.

---

## 5. How to run it (step by step)

> The bundled `venv/` was built on another machine — make a fresh one in step 2.

```powershell
# 1. Open a terminal in this folder (the one with manage.py)

# 2. Create a virtual environment and install Django
python -m venv venv
venv\Scripts\activate          # Windows  (macOS/Linux: source venv/bin/activate)
pip install "Django>=6.0,<6.1"

# 3. Apply database migrations
python manage.py migrate

# 4. Start the server
python manage.py runserver
```

Then open:
- Public blog (home): **http://127.0.0.1:8000/**
- Site login: **http://127.0.0.1:8000/accounts/login/**
- Admin panel: **http://127.0.0.1:8000/admin/**  (login `admin` / `admin`)

### If you start from an empty database
This project has **no seed script**. The shipped `db.sqlite3` already contains the
`admin` / `admin` user and a sample post. If you ever delete the database and need
to recreate the admin account, run this one-liner (it sets the password to
`admin`):

```powershell
python manage.py shell -c "from django.contrib.auth.models import User; u,_=User.objects.get_or_create(username='admin', defaults={'email':'admin@example.com','is_staff':True,'is_superuser':True}); u.is_staff=True; u.is_superuser=True; u.set_password('admin'); u.save(); print('admin/admin ready')"
```
(Or use the interactive `python manage.py createsuperuser`.)

---

## 6. How to test it

This project ships a **12-test Django suite** (models + views + permissions):

```powershell
python manage.py test
```

Expected result:
```
Ran 12 tests in ~11s
OK
```

Highlights of what is tested: published-only listing, category filtering, the
author **dashboard** (redirect when logged out), creating a post, an author
updating their own post (allowed), a different user trying to edit it (**403
Forbidden**), and adding a comment.

---

## 7. URL / route reference

| URL | View | Login? | Purpose |
|-----|------|--------|---------|
| `/` | `PostListView` | No | All **published** posts |
| `/category/<slug>/` | `CategoryPostListView` | No | Posts in one category |
| `/post/<slug>/` | `PostDetailView` | No | One post + its comments |
| `/post/new/` | `PostCreateView` | **Yes** | Write a new post |
| `/post/<slug>/edit/` | `PostUpdateView` | **Yes (author)** | Edit your own post |
| `/post/<slug>/comment/` | `add_comment` | **Yes** | Add a comment |
| `/dashboard/` | `AuthorDashboardView` | **Yes** | Your own posts |
| `/accounts/login/` `/logout/` | Django auth | — | Log in / out |
| `/admin/` | Django Admin | **Yes (admin)** | Manage everything |

---

## 8. Things to try

1. Log in as `admin` / `admin`, open **`/post/new/`** and publish a post.
2. In `/admin/`, create a **second user**, log in as them, and try to edit the
   admin's post via its `/edit/` URL → you should get **403 Forbidden** (the
   author-only rule in action).
3. Create a **Draft** post and confirm it does **not** appear on the public home
   page, but **does** appear in your dashboard.
4. Add a `DeleteView` so authors can delete their own posts (good exercise!).

---

## 9. Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'django'` | Activate the venv and `pip install Django` (step 2). |
| Login page is blank / TemplateDoesNotExist | Make sure `templates/registration/login.html` exists (it does). |
| Can't log in with `admin` / `admin` | Recreate it with the one-liner in section 5. |
| Editing someone else's post gives 403 | That's correct behaviour, not a bug. |
| Port 8000 in use | `python manage.py runserver 8001`. |

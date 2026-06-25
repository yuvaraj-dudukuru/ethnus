# ✍️ Project 3 — Blog Management Dashboard (Module 6)

A small, **fully working web dashboard** for a blog. It is the **front-end** (the
part you see and click) built on top of the REST API from Module 5. Nothing on
the page ever reloads — when you like a post, open its comments or publish a new
post, JavaScript quietly talks to the API in the background (**AJAX**) and
updates the screen instantly.

> **In one sentence:** Module 5 built the *engine* (a JSON API); Module 6 builds
> the *dashboard* that drives it live in the browser.

**⭐ The star feature** of this project is the **optimistic "like" button**: the
heart count goes up the **instant** you click, the request is sent in the
background, and the number **rolls back** only if the server says no. That is the
trick that makes apps feel instant.

Every file is **heavily commented** so you can read it and understand exactly
what each line does. Clone it, run it in a few minutes, and experiment.

---

## 📑 Table of Contents
1. [What is this project?](#-1-what-is-this-project)
2. [What can it do? (features)](#-2-what-can-it-do-features)
3. [Logins & passwords (everything you need)](#-3-logins--passwords-everything-you-need)
4. [Requirements](#-4-requirements)
5. [How to run it (step by step)](#-5-how-to-run-it-step-by-step)
6. [How to use the dashboard](#-6-how-to-use-the-dashboard)
7. [How to stop it](#-7-how-to-stop-it)
8. [How it works (cards, comments, optimistic likes)](#-8-how-it-works-cards-comments-optimistic-likes)
9. [Project structure (what each file is)](#-9-project-structure-what-each-file-is)
10. [Watch it work: the Network tab](#-10-watch-it-work-the-network-tab)
11. [Troubleshooting](#-11-troubleshooting)

---

## 📖 1. What is this project?

It is a **single-page dashboard** that runs in your web browser. It shows a feed
of blog posts as **cards**, and lets you:

- **Read** every published post.
- **Like** a post (optimistic UI — the star feature).
- **Open the comments** on any post and **add** your own.
- **Write & publish** a new post (or save it as a draft).
- **Search** posts as you type.

The page itself ([blog/templates/blog/dashboard.html](blog/templates/blog/dashboard.html))
is almost empty — it only draws the frame and a hidden card **template**. All the
real action lives in one JavaScript file
([static/js/dashboard.js](static/js/dashboard.js)), which clones the template for
each post and talks to the API.

---

## ✨ 2. What can it do? (features)

| Feature | What you do | What happens behind the scenes |
|---|---|---|
| **Post cards** | Open the page | `GET /api/posts/` → each post is mapped to a card (all text escaped) |
| **Live search** | Type in the search box | `GET /api/posts/?search=django` (debounced) |
| **Pagination** | **Newer / Older** | `GET /api/posts/?page=2` |
| **Open comments** | Click **💬 Comments** | `GET /api/posts/<slug>/comments/` → appended under the card |
| **Add a comment** | Type + **Send** | `POST /api/posts/<slug>/comments/` → added to the list, no reload |
| **Like** ⭐ | Click the heart | Count rises **instantly**, then `POST /api/posts/<slug>/like/`; rolls back on error |
| **Write a post** | Fill the form → **Publish** | `POST /api/posts/` (you are stamped as the author) |
| **Auth gate** | (automatic) | The page asks `GET /api/me/` and only shows like/comment/write to logged-in users |

**Reading is public.** Liking, commenting and writing require a **login**.

---

## 🔑 3. Logins & passwords (everything you need)

This is a **learning project**, so the passwords are deliberately simple and are
listed here on purpose. **Never use passwords like these on a real website.**

| Who | Username | Password | What it can do |
|---|---|---|---|
| **Admin** | `admin` | `admin` | Everything, plus the Django admin panel |
| **Writer** | `writer` | `writer` | A normal author: like, comment, write posts, edit **their own** posts |

- Both accounts are created automatically by the `seed` command (step 4) — you
  do **not** create them yourself.
- **To like, comment or write, log in** with either account in the top bar.
- `admin / admin` also works at the Django admin panel:
  <http://127.0.0.1:8000/admin/>.

> The seed also adds a **draft** post owned by `writer`. Drafts are hidden from
> the public feed — log in as `writer` to see how only published posts appear.

---

## 🧰 4. Requirements

- **Python 3.10 or newer** (tested on 3.13). Check with `python --version`.
- That's it. Everything else is installed from
  [requirements.txt](requirements.txt) in step 4.
- An internet connection the **first time** you open the page (Bootstrap loads
  from a CDN).

The database is **SQLite** — a tiny file (`db.sqlite3`) created automatically.

---

## ▶️ 5. How to run it (step by step)

Open a terminal **inside the `project_3` folder** and run these in order.
(On **Windows** use the PowerShell lines; on **macOS/Linux** use the others.)

### Step 1 — Create a virtual environment

```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

When it works, your prompt shows `(venv)`.

### Step 2 — Install the libraries

```bash
#check requirements.txt
```

### Step 3 — Create the database tables

```bash
python manage.py migrate
```

### Step 4 — Create the accounts + sample posts

```bash
python manage.py seed
```

This creates `admin / admin` and `writer / writer`, plus sample categories,
posts and a comment. Safe to run more than once.

### Step 5 — Start the server

```bash
python manage.py runserver
```

### Step 6 — Open the dashboard

Go to:

> **<http://127.0.0.1:8000/>**

You should see the **Blog Management Dashboard** with a feed of post cards. 🎉

---

## 🖱️ 6. How to use the dashboard

1. **Read the feed.** Each post is a card with its author, category and date.
2. **Log in** to unlock actions: top bar → `writer` / `writer` (or `admin`).
3. **Like a post:** click the 🤍 heart. The count jumps up immediately (that's
   the optimistic UI). If the server were unreachable, it would quietly roll
   back.
4. **Comments:** click **💬 Comments** on a card to load them. When logged in, a
   small box appears — type a comment and click **Send**; it's added instantly.
5. **Write a post:** when logged in, the **"Write a new post"** form appears at
   the top. Add a title, optional category and body. Leave *Publish now* ticked
   to publish, or untick it to save a hidden **draft**.
6. **Search:** type in the 🔍 box to filter posts.

Green messages mean success; red messages explain any error.

---

## ⏹️ 7. How to stop it

- In the terminal running the server, press **`Ctrl` + `C`**.
- To leave the virtual environment, type `deactivate`.
- Your data stays saved in `db.sqlite3`. Next time, just `activate` and
  `python manage.py runserver` again.

---

## 🔄 8. How it works (cards, comments, optimistic likes)

### Post cards (map → template, escaped)

The API returns a list of post objects. The JavaScript **maps** each one to a
card by cloning a hidden `<template>` in the HTML and filling in the blanks. All
user text (titles, names, comment bodies) is **escaped** first, so it can never
break the page or inject markup.

### Comments per post (no reload)

Each card has its own comments area. The first time you open it, the JS fetches
`GET /api/posts/<slug>/comments/` and lists them. When you post a new comment
(`POST` to the same URL), the returned comment is simply **appended** to the list
— the page never reloads.

### ⭐ Optimistic likes (the star pattern)

```
  You click 🤍
      │
      ├─ 1. INSTANTLY change the screen:  count + 1, heart turns ❤️   (optimistic)
      │
      ├─ 2. In the background:  POST /api/posts/<slug>/like/
      │
      ├─ 3a. Server says OK  → set the count to the server's real number
      └─ 3b. Server/network FAILS → ROLL BACK: undo the +1 and the red heart
```

The user sees an instant response and almost never notices the network. Rolling
back on failure keeps the screen honest. (To keep the teaching example simple,
every click adds a like; a real app would also track *who* liked *what*.)

### The auth gate (`/api/me/`)

This dashboard is a token-based single-page app, so it asks the API
**`GET /api/me/`** "who am I?". The reply (`{"is_authenticated": true,
"username": "writer"}` or `{"is_authenticated": false}`) decides which buttons
appear. Logging in stores a **token** that is sent on every write request.

---

## 🗂️ 9. Project structure (what each file is)

```
project_3/
├── manage.py                        # Django's command tool (runserver, migrate, seed…)
├── requirements.txt                 # Libraries to install
├── db.sqlite3                       # The database file (auto-created; not in Git)
├── README.md                        # This file
│
├── bloghub/                         # Project-wide configuration
│   ├── settings.py                  # All settings; M6 adds STATICFILES_DIRS
│   ├── urls.py                      # URL map; M6 adds "/" page + /api/me/
│   └── pagination.py                # "10 posts per page" rule
│
├── blog/                            # The blog app
│   ├── models.py                    # Category, Post, Comment; M6 adds Post.likes
│   ├── serializers.py               # Objects ↔ JSON; M6 adds 'likes' to both serializers
│   ├── api_views.py                 # ViewSets + comments; M6 adds 'like' action & MeView
│   ├── permissions.py               # IsOwnerOrReadOnly (only the author may edit) (M5)
│   ├── management/commands/seed.py  # The "python manage.py seed" helper         (M5)
│   ├── migrations/0002_post_likes.py# M6: adds the likes column
│   └── templates/blog/
│       └── dashboard.html           # ⭐ M6: the page SHELL + a card <template>
│
└── static/js/
    └── dashboard.js                 # ⭐ M6: ALL the front-end logic (AJAX)
```

**The two files Module 6 is really about** are marked ⭐. The rest is the
Module-5 API. The M6 backend additions are small and clearly commented:

1. `STATICFILES_DIRS` in `settings.py` (serve the JS).
2. A `/` dashboard route in `urls.py`.
3. A **`likes`** field on `Post` (+ migration `0002_post_likes`), exposed in the
   serializers, with a **`like` action** at `POST /api/posts/<slug>/like/`.
4. A **`/api/me/`** endpoint so the front-end can check who is logged in.

---

## 🔬 10. Watch it work: the Network tab

1. Open the dashboard, press **F12** → **Network** tab → tick **Fetch/XHR**.
2. Click a heart and watch the `like/` request fire *after* the number already
   changed on screen — that's the optimism.
3. Open a card's comments and watch the `comments/` request; add a comment and
   watch the `POST`.
4. On load, spot the `me/` request — that's the auth gate.

---

## 🛠️ 11. Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Try `python3`, or install Python 3. |
| Feed is empty | Did you run `python manage.py seed`? It creates the sample posts. |
| `(venv)` doesn't appear | The activate command didn't run — re-run step 1 for your OS. |
| Like / comment / write missing | Log in first — those are only shown to logged-in users (the auth gate). |
| Clicked a heart but it jumped back | That's the rollback — the server rejected it. Make sure you're logged in. |
| My new **draft** isn't in the feed | Drafts are hidden from the public feed on purpose. Publish it, or view it in the admin. |
| Page looks unstyled | Bootstrap loads from the internet — check your connection. |
| Port 8000 already in use | `python manage.py runserver 8001`, then open <http://127.0.0.1:8001/>. |
| Changed the JS but see no change | Hard-refresh: **Ctrl + F5**. |
| Want a fresh start | Stop the server, delete `db.sqlite3`, run `migrate` and `seed` again. |

---

### 📌 Bonus links (once the server is running)

- **Dashboard:** <http://127.0.0.1:8000/>
- **Interactive API docs (Swagger):** <http://127.0.0.1:8000/api/docs/>
- **Browsable API:** <http://127.0.0.1:8000/api/posts/>
- **Who am I?:** <http://127.0.0.1:8000/api/me/>
- **Admin panel:** <http://127.0.0.1:8000/admin/>  (`admin` / `admin`)

Happy learning! ✍️

# 🎓 Project 1 — Student Management Dashboard (Module 6)

A small, **fully working web dashboard** for managing college students. It is the
**front-end** (the part you see and click) built on top of the REST API we made
in Module 5. Everything happens **without the page ever reloading** — when you
search, add, edit or delete a student, JavaScript quietly talks to the API in
the background and updates the screen instantly. This technique is called
**AJAX**.

> **In one sentence:** Module 5 built the *engine* (a JSON API); Module 6 builds
> the *dashboard* (a web page) that drives that engine live in the browser.

This project is made for **students learning web development**. Every file is
**heavily commented** so you can open it, read it top-to-bottom, and understand
exactly what each line does. Clone it, run it in a few minutes, and experiment.

---

## 📑 Table of Contents
1. [What is this project?](#-1-what-is-this-project)
2. [What can it do? (features)](#-2-what-can-it-do-features)
3. [Logins & passwords (everything you need)](#-3-logins--passwords-everything-you-need)
4. [Requirements](#-4-requirements)
5. [How to run it (step by step)](#-5-how-to-run-it-step-by-step)
6. [How to use the dashboard](#-6-how-to-use-the-dashboard)
7. [How to stop it](#-7-how-to-stop-it)
8. [How it works (the AJAX flow)](#-8-how-it-works-the-ajax-flow)
9. [Project structure (what each file is)](#-9-project-structure-what-each-file-is)
10. [Watch it work: the Network tab](#-10-watch-it-work-the-network-tab)
11. [Troubleshooting](#-11-troubleshooting)

---

## 📖 1. What is this project?

It is a **single-page dashboard** that runs in your web browser. It shows a
table of students and lets you:

- **Search** students as you type.
- **Add** a new student with a small form.
- **Edit** a student's marks directly in the table.
- **Delete** a student.
- Move between **pages** of students.

The page itself ([students/templates/students/dashboard.html](students/templates/students/dashboard.html))
is almost empty — it only draws the frame (search box, empty table, buttons).
All the real action lives in one JavaScript file
([static/js/dashboard.js](static/js/dashboard.js)), which sends background
requests to the API and fills the page in.

The **API** it talks to (students, departments, login, etc.) is exactly the one
from Module 5 — reused **unchanged**. So this project teaches the front-end half
of a modern web app: **HTML + JavaScript talking to a REST API**.

---

## ✨ 2. What can it do? (features)

| Feature | What you do | What happens behind the scenes |
|---|---|---|
| **Load list** | Open the page | `GET /api/students/` → rows are drawn into the table |
| **Live search** | Type in the search box | After you pause typing (debounced), `GET /api/students/?search=...` |
| **Add student** | Fill the form, click **Add** | `POST /api/students/` with JSON; new student appears |
| **Edit marks** | Change the number, click 💾 | `PATCH /api/students/<id>/` updates only the marks |
| **Delete** | Click 🗑, confirm | `DELETE /api/students/<id>/` removes the student |
| **Pagination** | Click **Previous / Next** | `GET /api/students/?page=2` loads the next 10 |
| **Login** | Enter `admin / admin`, click **Login** | `POST /api/login/` returns a token used for edits |
| **Status feedback** | (automatic) | A spinner, green/red flash messages, and empty/error states |

**Reading is public** — anyone can view and search the list. **Writing** (add,
edit, delete) requires you to **log in** first (see below).

---

## 🔑 3. Logins & passwords (everything you need)

This is a **learning project**, so the passwords are deliberately simple and are
listed here on purpose. **Never use passwords like these on a real website.**

| Who | Username | Password | What it can do |
|---|---|---|---|
| **Admin** | `admin` | `admin` | Everything: add, edit, **and delete** students; also access the Django admin panel |

- The admin account is created automatically by the `seed` command (step 4
  below) — you do **not** need to create it yourself.
- **To edit anything on the dashboard you must log in** using the small login bar
  at the top of the page (`admin` / `admin`).
- The same `admin / admin` works at the Django admin panel:
  <http://127.0.0.1:8000/admin/>.

> **Note on deleting:** the API only lets the **admin** user delete students.
> Since `admin` is the only account here, just log in as admin and delete away.

---

## 🧰 4. Requirements

- **Python 3.10 or newer** (tested on 3.13). Check with `python --version`.
- That's it. Everything else (Django, DRF, etc.) is installed from
  [requirements.txt](requirements.txt) in step 4.
- An internet connection the **first time** you open the page (Bootstrap, the
  styling library, loads from a CDN).

The database is **SQLite** — a tiny file (`db.sqlite3`) created automatically.
No database server to install, no passwords to configure.

---

## ▶️ 5. How to run it (step by step)

Open a terminal **inside the `project_1` folder** and run these commands in
order. (On **Windows** use the PowerShell lines; on **macOS/Linux** use the
other lines.)

### Step 1 — Create a virtual environment (a private box for the libraries)

```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

After this your prompt shows `(venv)` at the start. That means it worked.

### Step 2 — Install the required libraries

```bash
#check requirements.txt
```

### Step 3 — Create the database tables

```bash
python manage.py migrate
```

### Step 4 — Create the admin user and some sample students

```bash
python manage.py seed
```

This creates the `admin / admin` account plus a few sample departments and
students, so the dashboard has data to show. It is safe to run more than once.

### Step 5 — Start the server

```bash
python manage.py runserver
```

### Step 6 — Open the dashboard

Open your web browser and go to:

> **<http://127.0.0.1:8000/>**

You should see the **Student Management Dashboard** with a table of students. 🎉

---

## 🖱️ 6. How to use the dashboard

1. **Look at the list.** When the page opens you see the first 10 students.
2. **Log in** to enable editing: in the top bar type `admin` / `admin` and click
   **Login**. (Without logging in you can still *view and search*, but Add/Edit/
   Delete will politely tell you to log in.)
3. **Search:** start typing a name, email or department in the 🔍 box. Results
   update automatically.
4. **Add a student:** fill the Roll / Name / Email / Marks / Department form and
   click **Add**. ⚠️ The email **must end in `@college.edu`** (an API rule), e.g.
   `john@college.edu`.
5. **Edit marks:** change the number in a student's **Marks** box and click the
   💾 button on that row.
6. **Delete:** click the 🗑 button on a row and confirm.
7. **Turn pages:** use **← Previous** and **Next →** at the bottom.

Green messages mean success; red messages explain any error.

---

## ⏹️ 7. How to stop it

- In the terminal where the server is running, press **`Ctrl` + `C`**. The
  server stops.
- To leave the virtual environment afterwards, type `deactivate`.
- Your data stays saved in `db.sqlite3`. Next time, just `activate` the venv and
  run `python manage.py runserver` again — no need to migrate or seed twice.

---

## 🔄 8. How it works (the AJAX flow)

The whole point of Module 6 is this loop, which never reloads the page:

```
  YOU (browser)                          SERVER (Django + DRF API)
  ─────────────                          ─────────────────────────
  1. Open the page  ───────────────────▶ sends dashboard.html (the empty frame)
  2. dashboard.js runs, then asks:
        GET /api/students/    ──────────▶ returns JSON: { count, results: [...] }
  3. JavaScript builds the table rows  ◀── (no page reload!)

  You click "Add" ─▶ POST /api/students/ (JSON) ─▶ saved ─▶ row appears
  You type a search ─▶ GET /api/students/?search=ali ─▶ matching rows redraw
  You edit marks ─▶ PATCH /api/students/5/ {marks:90} ─▶ updated
  You click delete ─▶ DELETE /api/students/5/ ─▶ row removed
```

**Login & tokens (why you log in):** the API lets anyone *read*, but only
logged-in users may *write*. When you log in, the page calls `POST /api/login/`
and gets back a **token** (a long secret string). The browser remembers it and
attaches it to every add/edit/delete request as proof of who you are. Logging
out simply forgets the token.

**The page envelope:** the list endpoint doesn't return a bare array — it returns
`{ "count": 25, "next": ..., "previous": ..., "results": [ ...10 students... ] }`.
The JavaScript reads `count` to work out how many pages exist and `results` to
draw the rows. This is standard DRF pagination.

---

## 🗂️ 9. Project structure (what each file is)

```
project_1/
├── manage.py                       # Django's command tool (runserver, migrate, seed…)
├── requirements.txt                # The list of libraries to install
├── db.sqlite3                      # The database file (auto-created; not in Git)
├── README.md                       # This file
│
├── campushub/                      # Project-wide configuration
│   ├── settings.py                 # All settings; M6 adds STATICFILES_DIRS
│   ├── urls.py                     # URL map; M6 adds the "/" dashboard page route
│   └── pagination.py               # "10 students per page" rule
│
├── students/                       # The students app
│   ├── models.py                   # Database design: Department & Student  (M5)
│   ├── serializers.py              # Turns objects ↔ JSON                   (M5)
│   ├── api_views.py                # The StudentViewSet (the API logic)     (M5)
│   ├── filters.py                  # ?min_marks=&department= filtering      (M5)
│   ├── admin.py                    # Registers models in the admin panel    (M5)
│   ├── management/commands/seed.py # The "python manage.py seed" helper     (M5)
│   └── templates/students/
│       └── dashboard.html          # ⭐ M6: the page SHELL (HTML frame only)
│
└── static/js/
    └── dashboard.js                # ⭐ M6: ALL the front-end logic (AJAX)
```

**The two files Module 6 is really about** are marked ⭐:
`dashboard.html` (the empty frame) and `dashboard.js` (the brain). Everything
else is the Module-5 API, reused as-is. The only backend tweaks for M6 are two
small, clearly-commented additions in `settings.py` and `urls.py`.

---

## 🔬 10. Watch it work: the Network tab

This is the best way to *understand* the project:

1. Open the dashboard in your browser.
2. Press **F12** to open DevTools, and click the **Network** tab.
3. Tick **Fetch/XHR** to filter to background requests.
4. Now use the page — type a search, add a student, edit marks. Each action
   shows up as a separate request (e.g. `students/?search=asha`). Click one to
   see exactly what JSON was sent and received.

You'll *see* the AJAX requests this whole project is built around.

---

## 🛠️ 11. Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Try `python3` instead, or install Python 3. |
| Page loads but the table is empty | Did you run `python manage.py seed`? It creates the sample students. |
| `(venv)` doesn't appear | The activate command didn't run — re-run step 1 for your OS. |
| Add/Edit/Delete says "please log in" | Click **Login** in the top bar with `admin` / `admin`. |
| "Official @college.edu email required" | The API only accepts emails ending in `@college.edu`. |
| The page looks unstyled (plain text) | Bootstrap loads from the internet — check your connection. |
| Port 8000 is already in use | Run on another port: `python manage.py runserver 8001`, then open <http://127.0.0.1:8001/>. |
| Changed the JS but see no difference | Hard-refresh the browser: **Ctrl + F5** (clears the cached file). |
| Want a totally fresh start | Stop the server, delete `db.sqlite3`, then run `migrate` and `seed` again. |

---

### 📌 Bonus links (once the server is running)

- **Dashboard:** <http://127.0.0.1:8000/>
- **Interactive API docs (Swagger):** <http://127.0.0.1:8000/api/docs/>
- **Browsable API:** <http://127.0.0.1:8000/api/students/>
- **Admin panel:** <http://127.0.0.1:8000/admin/>  (`admin` / `admin`)

Happy learning! 🎓

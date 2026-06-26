# 📊 Project 5 — Admin Analytics Dashboard (Module 6)

A small, **fully working analytics dashboard** for a college's student data. It
is the **front-end** built on top of the REST API from Module 5. The page draws
**charts** and **stat cards** from the database, all fetched in the background
(**AJAX**) — no page reloads.

> **In one sentence:** Module 5 built the *engine* (a JSON API); Module 6 turns
> the data into a picture — bar, line and doughnut charts plus headline numbers.

**⭐ The star skill** of this project is **transforming API JSON into chart
data**: the server sends arrays like `[{"label":"Physics","count":12}]`, and the
JavaScript maps them into the two parallel arrays Chart.js needs — `labels[]` and
`data[]`.

Every file is **heavily commented** so you can read it and understand exactly
what each line does. Clone it, run it in a few minutes, and experiment.

---

## 📑 Table of Contents
1. [What is this project?](#-1-what-is-this-project)
2. [What can it do? (features)](#-2-what-can-it-do-features)
3. [Logins & passwords](#-3-logins--passwords)
4. [Requirements](#-4-requirements)
5. [How to run it (step by step)](#-5-how-to-run-it-step-by-step)
6. [How to use the dashboard](#-6-how-to-use-the-dashboard)
7. [How to stop it](#-7-how-to-stop-it)
8. [How it works (one endpoint → many charts)](#-8-how-it-works-one-endpoint--many-charts)
9. [Project structure (what each file is)](#-9-project-structure-what-each-file-is)
10. [Troubleshooting](#-10-troubleshooting)

---

## 📖 1. What is this project?

It is a **single-page analytics dashboard** that runs in your web browser. It
shows, for the college's students:

- **Four stat cards:** total students, average marks, top scorer, active count.
- **A bar chart:** how many students are in each department.
- **A line chart:** how many students were admitted each month.
- **A doughnut chart:** how many students passed vs failed.
- **A date-range filter** that recalculates everything for a chosen period.

The page itself ([students/templates/students/dashboard.html](students/templates/students/dashboard.html))
is almost empty — it only draws the frame, empty chart canvases and grey
**skeleton loaders**. All the numbers come from one JavaScript file
([static/js/dashboard.js](static/js/dashboard.js)) calling **one** API endpoint.

---

## ✨ 2. What can it do? (features)

| Feature | What you see | What happens behind the scenes |
|---|---|---|
| **Stat cards** | Total / Average / Top scorer / Active | From `GET /api/stats/` → `cards` |
| **Bar chart** | Students per department | `by_department` → Chart.js `labels[]` + `data[]` |
| **Line chart** | Admissions per month | `admissions_by_month` (built with `TruncMonth`) |
| **Doughnut** | Pass vs Fail | `pass_fail` (marks ≥ 40 = pass) |
| **Date filter** | "Admitted from / to" | Re-calls `GET /api/stats/?start=&end=` and rebuilds everything |
| **Skeleton loaders** | Grey shimmer while loading | Hidden once the data arrives |

Everything on the page is fed by a **single** call to `/api/stats/`.

---

## 🔑 3. Logins & passwords

This dashboard is **read-only and public** — you do **not** need to log in to
view the charts. An admin account is still created for the Django admin panel
(where you can add/edit students and watch the charts change):

| Who | Username | Password | What it's for |
|---|---|---|---|
| **Admin** | `admin` | `admin` | The Django admin panel at `/admin/` |

> **Never use a password like `admin` on a real website.** It's fine here because
> this is a local learning project. On a real site you would also restrict
> analytics to staff only.

---

## 🧰 4. Requirements

- **Python 3.10 or newer** (tested on 3.13). Check with `python --version`.
- That's it. Everything else is installed from
  [requirements.txt](requirements.txt) in step 4.
- An internet connection the **first time** you open the page (Chart.js and
  Bootstrap load from a CDN).

The database is **SQLite** — a tiny file (`db.sqlite3`) created automatically.

---

## ▶️ 5. How to run it (step by step)

Open a terminal **inside the `project_5` folder** and run these in order.
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
pip install -r requirements.txt
```

### Step 3 — Create the database tables

```bash
python manage.py migrate
```

### Step 4 — Create the admin + 40 sample students

```bash
python manage.py seed
```

This makes `admin / admin` and **40 students** with varied marks, spread across
four departments and the last six months — so all the charts have a real shape.

### Step 5 — Start the server

```bash
python manage.py runserver
```

### Step 6 — Open the dashboard

Go to:

> **<http://127.0.0.1:8000/>**

You should see the **Admin Analytics Dashboard** with cards and three charts. 🎉

---

## 🖱️ 6. How to use the dashboard

1. **Read the cards and charts.** They load with a short grey "skeleton"
   shimmer, then fill in.
2. **Filter by date:** pick an *Admitted from* and/or *Admitted to* date and
   click **Apply**. Every card and chart recalculates for just that period. Use
   **Reset** to go back to all dates.
3. **Watch the numbers change (optional):** open the Django admin
   <http://127.0.0.1:8000/admin/> (`admin` / `admin`), edit a student's marks or
   add a new student, then come back and **Apply** the filter (or refresh) — the
   charts update from the new data.

---

## ⏹️ 7. How to stop it

- In the terminal running the server, press **`Ctrl` + `C`**.
- To leave the virtual environment, type `deactivate`.

---

## 🔄 8. How it works (one endpoint → many charts)

### One aggregate endpoint

The dashboard is powered by a single endpoint, `GET /api/stats/`, which returns
everything at once:

```json
{
  "cards": { "total": 40, "average": 63.9, "active": 36,
             "top_scorer": {"name": "…", "marks": 99} },
  "by_department":       [ {"label": "Biology", "count": 14}, … ],
  "admissions_by_month": [ {"label": "Jan 2026", "count": 5}, … ],
  "pass_fail":           { "pass": 35, "fail": 5, "pass_mark": 40 }
}
```

Those numbers are computed **in the database** with Django's
`annotate()` / `aggregate()` (e.g. `Count`, `Avg`, and `TruncMonth` to group by
month) — not by looping in Python. Returning it all in one response means the
front-end refreshes the whole page with a single request.

### Reshaping JSON into chart data (the star skill)

Chart.js doesn't take an array of objects — it takes two parallel arrays. So for
each chart the JavaScript **maps** the results:

```js
// server: [ {label:"Physics", count:12}, {label:"Biology", count:14} ]
const labels = byDept.map(row => row.label);   // ["Physics","Biology"]
const data   = byDept.map(row => row.count);   // [12, 14]
new Chart(canvas, { type:'bar', data:{ labels, datasets:[{ data }] } });
```

That "reshape the API JSON into `labels[]`/`data[]`" step is the core job of any
charting front-end.

### The date filter re-fetches everything

Changing the dates just re-calls `/api/stats/?start=…&end=…`. The endpoint
filters students by admission date before aggregating, so the same code paints
the dashboard for any period.

### Skeleton loaders

Before the request, the page shows grey shimmer blocks where the cards and charts
will be. When the data arrives, the skeletons are hidden and the real content
appears — so the user never stares at a blank page.

---

## 🗂️ 9. Project structure (what each file is)

```
project_5/
├── manage.py                        # Django's command tool (runserver, migrate, seed…)
├── requirements.txt                 # Libraries to install
├── db.sqlite3                       # The database file (auto-created; not in Git)
├── README.md                        # This file
│
├── campushub/                       # Project-wide configuration
│   ├── settings.py                  # All settings; M6 adds STATICFILES_DIRS
│   └── urls.py                      # URL map; M6 adds "/" page + /api/stats/
│
├── students/                        # The students app
│   ├── models.py                    # Department & Student (marks, admitted…)   (M5)
│   ├── serializers.py               # Objects ↔ JSON                            (M5)
│   ├── api_views.py                 # ViewSets; M6 adds the StatsView aggregate
│   ├── filters.py                   # ?min_marks=&department= filtering          (M5)
│   ├── management/commands/seed.py  # M6: makes 40 chart-friendly students
│   └── templates/students/
│       └── dashboard.html           # ⭐ M6: the page SHELL (cards + canvases + skeletons)
│
└── static/js/
    └── dashboard.js                 # ⭐ M6: fetch /api/stats/ → cards + Chart.js charts
```

**The two files Module 6 is really about** are marked ⭐. The rest is the
Module-5 student API. The M6 backend additions are small and clearly commented:

1. `STATICFILES_DIRS` in `settings.py` (serve the JS).
2. A `/` dashboard route in `urls.py`.
3. A **`StatsView`** at `/api/stats/` built with `annotate()`/`aggregate()`,
   accepting an optional `?start=&end=` date range.
4. A richer **seed** so the charts have a meaningful shape.

---

## 🛠️ 10. Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Try `python3`, or install Python 3. |
| Charts are empty / all zero | Did you run `python manage.py seed`? It creates the 40 students. |
| `(venv)` doesn't appear | The activate command didn't run — re-run step 1 for your OS. |
| Charts never appear (just skeletons) | Chart.js loads from the internet — check your connection, then hard-refresh (**Ctrl + F5**). |
| Date filter shows nothing | Your range may be outside the seeded months — click **Reset**. |
| Page looks unstyled | Bootstrap loads from the internet — check your connection. |
| Port 8000 already in use | `python manage.py runserver 8001`, then open <http://127.0.0.1:8001/>. |
| Want a fresh start | Stop the server, delete `db.sqlite3`, run `migrate` and `seed` again. |

---

### 📌 Bonus links (once the server is running)

- **Dashboard:** <http://127.0.0.1:8000/>
- **The stats endpoint (raw JSON):** <http://127.0.0.1:8000/api/stats/>
- **With a date range:** <http://127.0.0.1:8000/api/stats/?start=2026-04-01&end=2026-06-30>
- **Interactive API docs (Swagger):** <http://127.0.0.1:8000/api/docs/>
- **Admin panel:** <http://127.0.0.1:8000/admin/>  (`admin` / `admin`)

Happy learning! 📊

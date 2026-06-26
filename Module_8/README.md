# 🚀 Module 8 — Production Deployment: Five Live Deployments

Welcome to Module 8. **There are (almost) no new apps here.** Instead, you take
the apps you already built in Modules 4–6 and **put them on the public internet** —
real URLs, real PostgreSQL databases, HTTPS, static/media handling, error
tracking and CI/CD. This is the module that turns *"it works on my machine"* into
*"here's the link."*

> **In one sentence:** Modules 4–6 taught you to *build*. Module 7 taught you to
> *collaborate*. Module 8 teaches you to **ship to production** — the difference
> between a folder of code and a product people can use.

Every project here is **already deployment-configured and verified to run**
(Django system checks pass, migrations apply, the REST API test suite is green).
You only need to push to GitHub and click through Render to make them live.

---

## 🎚️ The five deployments (do them in order)

```
 SIMPLE ──────────────────────────────────────────────▶ FULL PRODUCTION ─────▶ THE RESUME LINK

 🟢 P1            🟡 P2              🔵 P3              🟠 P4               🔴 P5
 Blog             Student Mgmt       REST API           E-Commerce          Portfolio
 (the template)   (media → S3)       (CI/CD + Swagger)  (flagship, secure)  (links them all)
   │                │                  │                  │                   │
   │ env settings   │ ephemeral disk   │ GitHub Actions   │ HSTS, secure      │ custom domain
   │ Postgres       │ lesson + S3      │ green-gated      │ cookies, Sentry,  │ 404 + SEO
   │ WhiteNoise     │ persistent media │ deploys, Postman │ staging, backups  │ GitHub Pages
```

| # | Project | Built from | New production muscle |
|---|---------|-----------|------------------------|
| 🟢 **1** | [Deploy Blog](./project_1_deploy_blog/) | Module 4 blog | The full Render pipeline: env config, Postgres, WhiteNoise, Gunicorn |
| 🟡 **2** | [Deploy Student Management](./project_2_deploy_student_management/) | Module 4 student app | **User-uploaded media** — the ephemeral-disk lesson + Amazon S3 fix |
| 🔵 **3** | [Deploy REST API](./project_3_deploy_rest_api/) | Module 5 DRF API | **CI/CD** with GitHub Actions, Swagger docs, Postman, CORS |
| 🟠 **4** | [Deploy E-Commerce](./project_4_deploy_ecommerce/) | Module 4 store | **Full production**: security hardening, S3, Sentry, staging, DB backups |
| 🔴 **5** | [Deploy Portfolio](./project_5_deploy_portfolio/) | Module 3 portfolio | **Custom domain**, HTTPS, 404, SEO — the live link on your resume |

---

## 🔑 Credentials cheat-sheet (all in one place)

> ⚠️ These are **demo** credentials for learning. Change them on any real public deploy.

| Project | Admin user | Password | Admin URL |
|---------|-----------|----------|-----------|
| 1 · Blog | `admin` | `Admin@12345` | `/admin/` |
| 2 · Student Mgmt | `admin` | `Admin@12345` (or `admin` via `seed.py`) | `/admin/` |
| 3 · REST API | `admin` | `admin` (via `manage.py seed`) | `/admin/` · token at `POST /api/login/` |
| 4 · E-Commerce | `admin` | `Admin@12345` (or `admin` via `seed.py`) | `/admin/` |
| 5 · Portfolio | — | *static site, no login* | — |

Each project's own `README.md` repeats its credentials, environment variables and
any AWS/Sentry IDs you need to fill in.

---

## 🧠 The mental model (read this once)

Every Django deployment here follows the **same shape**. Learn it once, repeat it
four times:

```
   YOUR REPO (GitHub)                 RENDER (the cloud)
   ─────────────────                  ──────────────────
                                    ┌───────────────────────────┐
   code + render.yaml ──push──▶     │  Web Service (Gunicorn)    │
   requirements.txt                 │   ./build.sh:              │
   build.sh                         │     pip install            │
   .env.example  (no secrets!)      │     collectstatic ─▶ WhiteNoise serves CSS/JS
        │                           │     migrate                │
        │  env vars set in          │   gunicorn …wsgi:application│
        ▼  the dashboard            │            │               │
   SECRET_KEY, DEBUG=False,         │            ▼               │
   ALLOWED_HOSTS, DATABASE_URL ────▶│   PostgreSQL add-on (data) │
                                    │   S3 (uploaded media)      │
                                    └───────────────────────────┘
```

- **`settings.py` reads everything from the environment** — the same code runs
  locally on SQLite (`DEBUG=True`) and live on Postgres (`DEBUG=False`).
- **WhiteNoise** serves static files from the web process (no separate CDN needed).
- **`dj-database-url`** turns Render's `DATABASE_URL` into Django's database config.
- **The web filesystem is ephemeral** — uploaded files must go to **S3** to survive
  redeploys (Projects 2 & 4).
- **Secrets never enter git** — `.env` is gitignored; only `.env.example` is committed.

---

## 🗂️ What's inside each Django project folder

Every project ships the standard Render deployment kit:

| File | What it does |
|------|--------------|
| `requirements.txt` | Pinned deps incl. `gunicorn`, `whitenoise`, `dj-database-url`, `psycopg2-binary` |
| `build.sh` | `pip install` → `collectstatic` → `migrate` (Render's Build Command) |
| `Procfile` | `web: gunicorn <project>.wsgi:application` (the Start Command) |
| `render.yaml` | One-click **Blueprint**: web service + Postgres (+ staging for P4) |
| `.env.example` | Documents every env var; copy to `.env` for local dev |
| `.gitignore` | Keeps secrets, venvs and build artifacts out of git |
| `runtime.txt` / `.python-version` | Pin Python 3.12.6 |
| `README.md` | Full walkthrough, credentials, testing & troubleshooting |

Plus per-project extras: **P3** adds `.github/workflows/tests.yml` + `postman_collection.json`;
**P5** adds `404.html`, `CNAME`, `robots.txt`, `sitemap.xml`, a Pages workflow.

---

## 🧰 Tech stack & versions

`Django 5.2.6` · `gunicorn 23` · `whitenoise 6.8` · `dj-database-url 2.3` ·
`psycopg2-binary 2.9` · `python-dotenv 1.0` · `Pillow 11` (media projects) ·
`djangorestframework 3.16` + `drf-spectacular` + `django-filter` + `django-cors-headers` (P3) ·
`django-storages` + `boto3` (S3, P2/P4) · `sentry-sdk` (P4). Python **3.12.6**.

---

## ✅ How to use this module

1. **Run any project locally first** (each README's "Run locally" section) — confirm
   it works before deploying.
2. **Push to GitHub** (Module 7 skills).
3. **Create a Render account** (free tier is enough for all of these).
4. **Deploy P1** following its README top-to-bottom — it's the full walkthrough the
   others build on.
5. **Deploy P2 → P4**, each adding one production concept (media, CI/CD, security).
6. **Deploy P5** and paste your four live URLs into its project cards.

By the end you'll have **five public URLs** — a blog, a CRUD app with uploads, a
documented REST API, an e-commerce store, and a portfolio that links them all —
behind one custom domain at the top of your resume. That's the most credible thing
a junior developer can show.

Happy shipping! 🚀

---

### 📌 Note on "everything works"
Because Render deployments require *your* account and a live click-through, the
code here is **deployment-ready and locally verified** (system checks pass,
migrations apply, tests are green, static collects, admin users created). The
READMEs give the exact dashboard steps to take each one live. Nothing is stubbed —
push and deploy.

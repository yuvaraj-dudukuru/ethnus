# 🟢 Project 1 — Deploy the Blog Application (Render)

This is the **full walkthrough** deployment of the Module 4 Blog app. It takes a
Django project that only ran on `127.0.0.1` and turns it into a **live, HTTPS
website on Render** backed by **PostgreSQL**, with static files served by
**WhiteNoise**. The exact same code runs locally (SQLite) and in production
(Postgres) — only environment variables change.

> **Live URL (fill in after you deploy):** `https://blog-app.onrender.com`

---

## 🔑 1. Credentials & IDs (READ THIS)

These are the demo accounts shipped in `db.sqlite3` and recreated on the live
server. **Change the password on any real public deployment.**

| What | Value |
|------|-------|
| **Admin username** | `admin` |
| **Admin password** | `Admin@12345` |
| **Admin email** | `admin@example.com` |
| **Django admin panel** | `/admin/` |
| **Site login page** | `/accounts/login/` |

The same `admin` / `Admin@12345` account is both the **superuser** (for `/admin/`)
and a normal site user (it can author posts and comments).

> 🔒 `Admin@12345` is a *demo* password chosen to satisfy Django's password
> validators while staying easy to type. Never reuse it on a production app you
> actually care about.

### Environment variables (set in Render → Environment)

| Key | Example value | Notes |
|-----|---------------|-------|
| `SECRET_KEY` | *(50+ random chars)* | Use Render's **Generate** button, or `get_random_secret_key()`. |
| `DEBUG` | `False` | Must be `False` in production. |
| `ALLOWED_HOSTS` | `blog-app.onrender.com` | Your Render hostname (comma-separated for more). |
| `DATABASE_URL` | `postgres://…` | Auto-filled from the Render Postgres add-on. |

---

## ✅ 2. Pre-deployment checklist

All of these are **already done** in this folder — verify them before you push:

- [x] `DEBUG` reads from env (`False` in prod) — `config/settings.py`
- [x] `SECRET_KEY` from env
- [x] `ALLOWED_HOSTS` includes the `.onrender.com` host (+ auto `RENDER_EXTERNAL_HOSTNAME`)
- [x] `requirements.txt` pinned (+ `gunicorn`, `psycopg2-binary`, `whitenoise`, `dj-database-url`)
- [x] WhiteNoise middleware + `STATIC_ROOT` set
- [x] `DATABASE_URL` parsed via `dj-database-url`
- [x] `.env` gitignored; `.env.example` committed
- [x] `python manage.py check --deploy` is clean (only warns about a weak key — Render's generated key fixes that)

---

## 🚀 3. Deployment steps (Render)

You can deploy **manually** (clicking in the dashboard) or **via the Blueprint**
(`render.yaml`). Manual steps:

1. **Push to GitHub** (Module 7 covered this).
2. **Create the database:** Render Dashboard → **New → PostgreSQL** → name it
   `blog-db` → Create. Copy the **Internal Database URL**.
3. **Create the web service:** **New → Web Service** → connect your repo.
   - **Build Command:**
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
     (or just `./build.sh`, which does the same three steps)
   - **Start Command:**
     ```
     gunicorn config.wsgi:application
     ```
4. **Add environment variables** (table above). Paste the Internal Database URL
   into `DATABASE_URL`.
5. **Deploy.** Watch the **Logs** tab until you see `Booting worker`.
6. **Create the admin user** — open the Render **Shell** tab and run:
   ```bash
   python manage.py createsuperuser
   ```
   (or paste the one-liner in §6 to recreate `admin` / `Admin@12345`).

### Blueprint alternative
Commit `render.yaml` (already here), then Dashboard → **New → Blueprint** →
pick your repo. Render creates the database **and** web service and wires
`DATABASE_URL` automatically.

---

## 🧪 4. Testing the live site

- Visit the live URL → the post list loads.
- Confirm the **🔒 padlock** (HTTPS) — Render gives every service a free cert.
- Confirm **CSS loads** (styled page, not raw HTML) → WhiteNoise + collectstatic working.
- Log into `/admin/` with `admin` / `Admin@12345`.
- **Create a post** and **add a comment**; refresh to confirm it persisted in Postgres.

---

## 🛠️ 5. Troubleshooting

| Symptom | Cause → Fix |
|---------|-------------|
| Page loads but **unstyled** | WhiteNoise/collectstatic — confirm `collectstatic` ran in the build and `STATIC_ROOT` is set. |
| **500 Server Error** | Check the **Logs** tab. Usually a missing migration or env var. |
| **DisallowedHost** error | Add your hostname to the `ALLOWED_HOSTS` env var and redeploy. |
| **CSRF 403** on login/forms | Hostname must be in `ALLOWED_HOSTS`; `CSRF_TRUSTED_ORIGINS` already covers `*.onrender.com`. |
| Build fails on `psycopg2` | Ensure `psycopg2-binary` is in `requirements.txt` (it is). |

---

## 💻 6. Run it locally

```bash
python -m venv venv
venv\Scripts\activate            # Windows (use: source venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
copy .env.example .env           # then edit values (or leave defaults for SQLite)
python manage.py migrate
python manage.py runserver
```
Visit http://127.0.0.1:8000/ . Admin: http://127.0.0.1:8000/admin/ (`admin` / `Admin@12345`).

Recreate the admin account any time:
```bash
python manage.py shell -c "from django.contrib.auth.models import User; u,_=User.objects.get_or_create(username='admin', defaults={'email':'admin@example.com'}); u.is_staff=True; u.is_superuser=True; u.set_password('Admin@12345'); u.save(); print('admin / Admin@12345 ready')"
```

---

## 📁 7. What changed for deployment (vs. Module 4)

| File | Change |
|------|--------|
| `config/settings.py` | `SECRET_KEY`/`DEBUG`/`ALLOWED_HOSTS`/`DATABASE_URL` from env; WhiteNoise middleware + `STATIC_ROOT` + compressed manifest storage; HTTPS/HSTS/secure-cookie hardening when `DEBUG=False`. |
| `requirements.txt` | Added `gunicorn`, `whitenoise`, `dj-database-url`, `psycopg2-binary`, `python-dotenv`. |
| `build.sh` | Install + collectstatic + migrate, run by Render on each deploy. |
| `render.yaml` | One-click Blueprint (web service + Postgres). |
| `Procfile` | `web: gunicorn config.wsgi:application`. |
| `.env.example` / `.gitignore` | Document env vars; keep real secrets out of git. |
| `runtime.txt` / `.python-version` | Pin Python 3.12.6. |

This is the template every other Module 8 project builds on.

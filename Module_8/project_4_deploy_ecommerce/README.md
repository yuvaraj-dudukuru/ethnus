# 🟠 Project 4 — Deploy the E-Commerce Application (Render, full production)

The **flagship** deployment. Everything from Projects 1–3 plus the concerns a real
**money app** has: PostgreSQL orders, session carts, authenticated checkout,
**persistent product images on S3**, a strict **security checklist**, **Sentry
error tracking**, **database backups before migrations**, and a **staging
environment** you promote to production after QA.

> **Production URL:** `https://ecommerce-store.onrender.com`
> **Staging URL:** `https://ecommerce-store-staging.onrender.com`

---

## 🔑 1. Credentials & IDs

| What | Value |
|------|-------|
| **Admin username** | `admin` |
| **Admin password** | `Admin@12345` (documented demo) / `admin` if created via `seed.py` |
| **Admin email** | `admin@example.com` |
| **Admin panel** | `/admin/` |
| **Store login** | `/login/` |

> `python seed.py` creates `admin` / `admin` + a catalogue (Smartphone X,
> Wireless Headphones, Cotton T-Shirt, Denim Jeans). The shipped `db.sqlite3`
> here uses the stronger `admin` / `Admin@12345`. Use whichever the message in
> your deploy log shows; change it on a real store.

### Environment variables (Render → Environment)

| Key | Example | Notes |
|-----|---------|-------|
| `SECRET_KEY` | *(50+ random)* | Render **Generate**. |
| `DEBUG` | `False` | |
| `ALLOWED_HOSTS` | `ecommerce-store.onrender.com` | |
| `DATABASE_URL` | `postgres://…` | Postgres add-on. |
| `USE_S3` | `True` (real) / `False` (demo) | Persistent product images. |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | *(IAM)* | If `USE_S3=True`. **secret!** |
| `AWS_STORAGE_BUCKET_NAME` / `AWS_S3_REGION_NAME` | `ecommerce-media` / `us-east-1` | If `USE_S3=True`. |
| `SENTRY_DSN` | `https://…ingest.sentry.io/…` | Error tracking (optional). |
| `ENVIRONMENT` | `production` / `staging` | Tags Sentry events. |

---

## 🔒 2. Security checklist (money app — do not skip)

All enforced in `ecommerce/settings.py` when `DEBUG=False`:

- [x] `SECURE_SSL_REDIRECT` — force HTTPS
- [x] `SECURE_HSTS_SECONDS = 31536000` + preload/subdomains — HSTS
- [x] `SESSION_COOKIE_SECURE` + `CSRF_COOKIE_SECURE` — cookies only over HTTPS
- [x] `SESSION_COOKIE_HTTPONLY` + `CSRF_COOKIE_HTTPONLY`
- [x] `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS = DENY`, referrer policy
- [x] `SECRET_KEY` from env, `DEBUG=False`, `ALLOWED_HOSTS` locked down
- [x] `python manage.py check --deploy` clean (with a real generated key)

---

## 💾 3. Database backups & migrations

A money app must never lose orders. **Before every migration on production:**
```bash
# Render dashboard: shop-db → Backups → "Create backup"  (or via pg_dump)
pg_dump "$DATABASE_URL" > backup_$(date +%F).sql
python manage.py migrate
```
Render's paid Postgres tiers add automatic daily backups + point-in-time
recovery; enable them for a real store.

---

## 🧫 4. Staging → Production workflow

`render.yaml` defines **two** services with **separate** databases:

```
feature branch ─PR─▶ staging branch ─▶ ecommerce-store-staging  (QA here)
                                              │  looks good?
                                              ▼
                         merge staging ─▶ main ─▶ ecommerce-store  (production)
```
Test the full purchase flow on staging first; only promote to `main` once green.

---

## 🖼️ 5. Product images (S3)

Same ephemeral-disk lesson as Project 2. `USE_S3=False` → images reset on
redeploy (demo only). For a real store set `USE_S3=True` + the `AWS_*` keys so
`django-storages` stores every product image on S3 permanently.

---

## ✅ 6. Pre-deployment checklist

- [x] env-driven `SECRET_KEY`/`DEBUG`/`ALLOWED_HOSTS`/`DATABASE_URL`
- [x] `requirements.txt` pinned (+ gunicorn/whitenoise/dj-database-url/psycopg2/**Pillow**/storages/boto3/sentry-sdk)
- [x] WhiteNoise + `STATIC_ROOT`
- [x] Security hardening (§2) · Media decided (§5) · Backups planned (§3) · Sentry wired (§1)
- [x] `.env` gitignored; `.env.example` committed
- [x] `python manage.py check` clean

---

## 🚀 7. Deployment steps

- **Build Command:** `./build.sh`  · **Start Command:** `gunicorn ecommerce.wsgi:application`
- Create Postgres, set env vars, deploy; or push `render.yaml` → **New → Blueprint**
  (creates prod + staging + both DBs).
- First deploy: Render **Shell** → `python seed.py` (catalogue + admin).

---

## 🧪 8. Testing

1. Browse catalogue → add to cart → cart count updates (context processor).
2. Log in / register → checkout (payments are mocked).
3. Confirm the **order persists in Postgres** (visible in `/admin/` → Orders).
4. Whole flow over **HTTPS** with the padlock; static + product images load.
5. Trigger an error → confirm it appears in **Sentry** (if `SENTRY_DSN` set).

---

## 🛠️ 9. Troubleshooting

| Symptom | Fix |
|---------|-----|
| Product images vanish after deploy | `USE_S3=False`; switch to S3. |
| `Pillow` import error | It's pinned in `requirements.txt`. |
| Mixed-content / cookie issues | Hardening requires HTTPS — fine on Render; locally keep `DEBUG=True`. |
| Lost data after a bad migration | Restore the backup from §3 — that's why you take one first. |
| 500s with no detail | Set `SENTRY_DSN`, or read the Render **Logs** tab. |

---

## 💻 10. Run locally

```bash
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python seed.py
python manage.py runserver
```
Store: http://127.0.0.1:8000/ · Admin: http://127.0.0.1:8000/admin/ (`admin` / `Admin@12345`).

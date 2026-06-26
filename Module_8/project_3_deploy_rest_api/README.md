# 🔵 Project 3 — Deploy the REST API (Render + CI/CD)

Deploys the Module 5 **Django REST Framework** API (CampusHub students) to Render,
gated behind a **GitHub Actions CI pipeline**: every push runs the `APITestCase`
suite, and only green builds get deployed. The interactive **Swagger docs** are
published at `/api/docs/`, and a **Postman collection** ships in this folder.

> **Live URL (fill in after you deploy):** `https://student-rest-api.onrender.com`
> **Swagger docs:** `https://student-rest-api.onrender.com/api/docs/`

---

## 🔑 1. Credentials & IDs

| What | Value |
|------|-------|
| **Admin username** | `admin` |
| **Admin password** | `admin` |
| **Admin email** | `admin@college.edu` |
| **Admin panel** | `/admin/` |
| **Token login endpoint** | `POST /api/login/` → `{ "token": "..." }` |

The `admin` / `admin` account is created by `python manage.py seed` (which also
loads 3 departments and 5 sample students). Use it to obtain a token.

### Token auth flow
```bash
# 1) Exchange username + password for a token
curl -X POST https://student-rest-api.onrender.com/api/login/ \
     -d "username=admin&password=admin"
# -> {"token":"9b1c...e4"}

# 2) Send that token on every write request
curl https://student-rest-api.onrender.com/api/students/ \
     -H "Authorization: Token 9b1c...e4" \
     -d "roll=201&name=New&email=n@c.edu&marks=90&department=1"
```

### Environment variables (Render → Environment)

| Key | Example | Notes |
|-----|---------|-------|
| `SECRET_KEY` | *(50+ random chars)* | Render **Generate**. |
| `DEBUG` | `False` | |
| `ALLOWED_HOSTS` | `student-rest-api.onrender.com` | |
| `DATABASE_URL` | `postgres://…` | From the Postgres add-on. |
| `CORS_ALLOWED_ORIGINS` | `https://my-frontend.com` | Comma-separated browser origins (optional). |

---

## 🌐 2. API endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `GET` | `/api/students/` | public | List students (paginated) |
| `POST` | `/api/students/` | **token** | Create a student |
| `GET/PUT/DELETE` | `/api/students/{id}/` | read public / write token | One student |
| `GET` | `/api/students/toppers/` | public | Custom action (top scorers) |
| `GET` | `/api/departments/` | public | List departments |
| `POST` | `/api/login/` | public | Get an auth token |
| `POST` | `/api/logout/` | token | Delete the token |
| `GET` | `/api/docs/` | public | Swagger UI |
| `GET` | `/api/schema/` | public | Raw OpenAPI schema |

Permissions are `IsAuthenticatedOrReadOnly`: anyone can **read**, only a
token-holder can **write**. Throttling: 100/hour anon, 2000/day user, 5/min login.

---

## ⚙️ 3. CI/CD pipeline (the delta vs. Projects 1–2)

`.github/workflows/tests.yml` runs on every push / PR to `main`:

```
push ──▶ GitHub Actions ──▶ pip install ──▶ manage.py check ──▶ manage.py test
                                                                   │
                                                  ✅ green ───▶ Render auto-deploys
                                                  ❌ red   ───▶ deploy blocked
```

To make the gate real:
1. In Render, set the service's **Auto-Deploy** to deploy on push.
2. In GitHub, add a **branch protection rule** on `main` → *Require status checks
   to pass* → select **API Tests**. Now a red test literally cannot be merged or
   shipped. Add the badge to your repo:
   `![CI](https://github.com/<you>/<repo>/actions/workflows/tests.yml/badge.svg)`

The suite (`students/tests.py`) verifies the public can list students (200) and
that anonymous writes are rejected (401) — exactly the production behaviour to
guarantee.

---

## ✅ 4. Pre-deployment checklist

- [x] `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL` from env
- [x] `requirements.txt` pinned (DRF stack + gunicorn/whitenoise/dj-database-url/psycopg2)
- [x] WhiteNoise serves the Swagger UI + browsable API + admin static
- [x] `django-cors-headers` configured for browser clients
- [x] GitHub Actions workflow runs the test suite
- [x] Postman collection committed (`postman_collection.json`)
- [x] `python manage.py test` passes (2/2) and `check` is clean

---

## 🚀 5. Deployment steps

- **Build Command:** `./build.sh`  (install → collectstatic → migrate)
- **Start Command:** `gunicorn campushub.wsgi:application`  *(unchanged from local)*
- After first deploy, open the Render **Shell** → `python manage.py seed` to create
  `admin`/`admin` + sample data.
- Or push `render.yaml` and use **New → Blueprint**.

---

## 🧪 6. Testing in production (Postman)

1. Import `postman_collection.json` into Postman.
2. Set the `base_url` variable to your `.onrender.com` URL.
3. Run **Login** → the token is captured automatically into `{{token}}`.
4. Verify:
   - `GET /api/students/` → **200** (public read works)
   - Create **with** token → **201**
   - Create **without** token → **401**
   - Hammer login 6×/min → **429 Too Many Requests** (throttle works in prod)

---

## 🛠️ 7. Troubleshooting

| Symptom | Fix |
|---------|-----|
| Swagger page unstyled | collectstatic / WhiteNoise (Project 1). |
| Browser client blocked by **CORS** | Add its origin to `CORS_ALLOWED_ORIGINS` and redeploy. |
| `401` on every write | You forgot the `Authorization: Token …` header. |
| `429` errors | Throttle limits hit — expected; back off or raise the rates. |
| Deploy shipped a bug | Add branch protection so red CI blocks the merge. |

---

## 💻 8. Run locally

```bash
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed
python manage.py runserver
python manage.py test        # run the suite locally before pushing
```
Docs: http://127.0.0.1:8000/api/docs/ · Admin: http://127.0.0.1:8000/admin/ (`admin`/`admin`).

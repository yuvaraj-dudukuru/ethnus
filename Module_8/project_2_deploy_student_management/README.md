# 🟡 Project 2 — Deploy the Student Management System (Render, media-aware)

Same deployment pipeline as Project 1 (Render + PostgreSQL + WhiteNoise + Gunicorn),
**plus the one new production concern this project exists to teach: user-uploaded
files** (student photos, `ImageField`). On Render the web filesystem is
**ephemeral** — uploads are deleted on every redeploy — so this project shows
both the demo behaviour *and* the real fix (Amazon S3).

> **Live URL (fill in after you deploy):** `https://student-management.onrender.com`

---

## 🔑 1. Credentials & IDs

| What | Value |
|------|-------|
| **Admin username** | `admin` |
| **Admin password** | `Admin@12345` |
| **Admin email** | `admin@example.com` |
| **Admin panel** | `/admin/` |
| **Login page** | `/accounts/login/` |

Seeded sample data (`python seed.py`): departments *Computer Science / IT /
Electronics* and students *Alice (roll 101), Bob (102), Charlie (103)*.

### Environment variables (Render → Environment)

| Key | Example | Notes |
|-----|---------|-------|
| `SECRET_KEY` | *(50+ random chars)* | Render **Generate** button. |
| `DEBUG` | `False` | |
| `ALLOWED_HOSTS` | `student-management.onrender.com` | |
| `DATABASE_URL` | `postgres://…` | From the Postgres add-on. |
| `USE_S3` | `False` (demo) / `True` (real) | Turns on S3 media storage. |
| `AWS_ACCESS_KEY_ID` | *(IAM key)* | Only if `USE_S3=True`. |
| `AWS_SECRET_ACCESS_KEY` | *(IAM secret)* | Only if `USE_S3=True`. **secret!** |
| `AWS_STORAGE_BUCKET_NAME` | `campushub-media` | Only if `USE_S3=True`. |
| `AWS_S3_REGION_NAME` | `us-east-1` | Only if `USE_S3=True`. |

---

## 📦 2. The media decision (the whole point of this project)

Render's disk is **ephemeral**. A photo uploaded through the student form lands in
`MEDIA_ROOT` (local disk) and **disappears on the next deploy**. You have two
choices, both supported by `campushub/settings.py`:

| Mode | `USE_S3` | What happens | Use when |
|------|----------|--------------|----------|
| **Demo** | `False` | Photos saved to local disk; reset on redeploy | Learning / showing the ephemeral lesson |
| **Real** | `True` | Photos saved to **Amazon S3**; survive forever | A deployment that actually keeps uploads |

☑️ **Media storage decided** — set `USE_S3` accordingly before you deploy.

### Enabling S3 (real deploy)
1. Create an S3 bucket (e.g. `campushub-media`) in your AWS account.
2. Create an IAM user with `s3:PutObject`/`GetObject`/`DeleteObject` on that bucket.
3. In Render set `USE_S3=True` and the four `AWS_*` vars above.
4. Redeploy. `django-storages` now writes every upload to S3, so photos persist.

---

## ✅ 3. Pre-deployment checklist

- [x] `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL` from env
- [x] `requirements.txt` pinned (+ `gunicorn`, `psycopg2-binary`, `whitenoise`, `dj-database-url`, **`Pillow`**)
- [x] WhiteNoise + `STATIC_ROOT`
- [x] **Media storage decided** (`USE_S3` toggle, `django-storages` + `boto3` available)
- [x] `.env` gitignored; `.env.example` committed
- [x] `python manage.py check` clean

---

## 🚀 4. Deployment steps

Identical to Project 1, with the start command pointing at this project's WSGI:

- **Build Command:** `./build.sh`  (install → collectstatic → migrate)
- **Start Command:** `gunicorn campushub.wsgi:application`
- After first deploy, open the Render **Shell** and run `python seed.py`
  (creates `admin`/`admin`) **or** `python manage.py createsuperuser`. To match
  this README's documented password run instead:
  ```bash
  python manage.py shell -c "from django.contrib.auth.models import User; u,_=User.objects.get_or_create(username='admin', defaults={'email':'admin@example.com'}); u.is_staff=True; u.is_superuser=True; u.set_password('Admin@12345'); u.save(); print('admin ready')"
  ```

Or just push `render.yaml` and use **New → Blueprint**.

---

## 🧪 5. Testing — prove the ephemeral lesson firsthand

1. Log in, add a student **with a photo**, confirm the photo displays.
2. **Trigger a redeploy** (push a commit or click *Manual Deploy*).
3. Re-open that student:
   - `USE_S3=False` → **photo is gone** (broken image). That's the ephemeral disk.
   - `USE_S3=True` → **photo still there**, served from S3. That's the fix.
4. Confirm HTTPS padlock and that CSS loads.

---

## 🛠️ 6. Troubleshooting

| Symptom | Fix |
|---------|-----|
| Uploaded photos vanish after deploy | Expected with `USE_S3=False`. Set `USE_S3=True` + S3 creds. |
| `cannot import name 'Image'` / ImageField error | `Pillow` missing — it's in `requirements.txt`. |
| S3 `AccessDenied` | IAM user lacks bucket permissions, or wrong bucket/region. |
| Unstyled page | collectstatic / WhiteNoise (see Project 1). |
| `DisallowedHost` | Add hostname to `ALLOWED_HOSTS`. |

---

## 💻 7. Run locally

```bash
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python seed.py            # admin/admin + sample students
python manage.py runserver
```
Then http://127.0.0.1:8000/ and /admin/ (`admin` / `Admin@12345`).

# 🎓 CampusHub API — Student Management REST API

A REST API for managing college students, built with **Django REST Framework**
(Module 5). Token auth, pagination, filtering, search, and interactive Swagger
docs.

![tests](https://github.com/<you>/campushub-api/actions/workflows/tests.yml/badge.svg)
<!-- ↑ this badge turns green/red automatically from your CI run -->

---

## 🚀 Run locally
```bash
git clone https://github.com/<you>/campushub-api.git
cd campushub-api
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed          # creates admin/admin + sample data
python manage.py runserver
```
Open <http://127.0.0.1:8000/api/docs/> for the interactive docs.

## 🔑 Authentication
Most reads are public; writes need a token.
```bash
# get a token
curl -X POST http://127.0.0.1:8000/api/login/ -d "username=admin&password=admin"
# use it
curl http://127.0.0.1:8000/api/students/ -H "Authorization: Token <your-token>"
```

## 📚 Endpoints
| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/api/students/` | public | List (paginated, `?search=`, `?department=`) |
| POST | `/api/students/` | token | Create a student |
| GET | `/api/students/{id}/` | public | Retrieve one |
| PATCH | `/api/students/{id}/` | token | Update |
| DELETE | `/api/students/{id}/` | admin | Delete |
| POST | `/api/login/` | public | Get an auth token |
| GET | `/api/docs/` | public | Swagger UI |

## 🧪 Run the tests
```bash
python manage.py test
```
CI runs these automatically on every push/PR (see `.github/workflows/tests.yml`).
A PR can't merge unless this suite is green ✔.

## 📄 License
MIT — see [LICENSE](LICENSE).

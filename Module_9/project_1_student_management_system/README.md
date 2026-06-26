# 🎓 Project 1 — Student Management System (CampusHub)

A full-stack capstone: a **Django + DRF** API with a **server-rendered + vanilla-JS**
dashboard for managing students, departments, courses and enrollments.

## What it does
- **Students**: full CRUD via the API, search, filter by department, marks.
- **Departments**: read-only API + live "strength" (student count).
- **Courses + Enrollments**: enrol a student in a course (`@action`), grades.
- **Dashboard**: live search, department filter, top-5 toppers chart, add-student form.
- **Auth/RBAC**: anyone can read; logged-in users can create/edit; only admins delete.

## Tech
Django 5.2 · Django REST Framework · django-filter · drf-spectacular (Swagger) ·
SQLite (local) / Postgres (prod) · WhiteNoise · Gunicorn.

## Run locally (Windows PowerShell)
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed          # creates admin/admin + demo data
python manage.py runserver
```
Open **http://127.0.0.1:8000/** (dashboard) · **/admin/** (admin/admin) ·
**/api/** (browsable API) · **/api/docs/** (Swagger).

## Key API endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/students/?search=&department=&min_marks=` | list/search/filter (public) |
| POST | `/api/students/` | create (login required) |
| DELETE | `/api/students/{id}/` | admin only |
| GET | `/api/students/toppers/` | top 5 active students |
| POST | `/api/students/{id}/enroll/` | body `{"course_id": 3}` (login required) |
| GET | `/api/departments/` | read-only, includes `strength` |
| GET/POST | `/api/courses/` | read public, write admin only |

## Testing
```powershell
python manage.py test
```
Covers public list, anonymous-write rejection, department strength, toppers order,
email-domain validation, duplicate-enrollment → 400, and admin-only delete.

## Deployment (Render — see Module 8)
`build.sh` + `Procfile` + `render.yaml` are included. Push to GitHub, create a Render
Blueprint from `render.yaml`, and set `DEBUG=False` + `DATABASE_URL`.

## Future scope
Attendance, timetable, email notifications, parent portal.

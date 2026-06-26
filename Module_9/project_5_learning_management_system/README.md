# 🧑‍🏫 Project 5 — Learning Management System (LearnSpace)

A full-stack **Django + DRF** LMS: instructors publish courses with ordered lessons;
students enrol and **track completion progress**.

## What it does
- **Courses & lessons** (ordered), authored by instructors (the creator owns the course).
- **Enroll** via `@action`; **mark lesson complete** via `@action`.
- **Progress %** computed per student per course.
- **Auth/RBAC**: read for all; logged-in users can create courses; only the owning
  instructor (or admin) may edit a course/its lessons.
- **Frontend**: course cards, lesson list, enrol button, completion toggles, progress bar.

## Run locally
```powershell
python -m venv venv; venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed   # admin/admin, instructor1/instructor, student1/student
python manage.py runserver
```
**/** courses · **/admin/** (admin/admin) · **/api/** · **/api/docs/**.

## Key endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/courses/?search=` | catalog (public) |
| POST | `/api/courses/{id}/enroll/` | enrol (login) |
| GET | `/api/courses/{id}/progress/` | your completion % |
| POST | `/api/lessons/{id}/complete/` | mark a lesson done |

## Testing
```powershell
python manage.py test
```
Covers: public catalog, **enroll + duplicate → 400**, **progress calculation (50%)**,
**instructor-only edit (403/200)**, and can't add lessons to someone else's course.

## Future scope
Quizzes, certificates, discussion forums, video hosting.

# 📝 Project 8 — Online Examination System (Examly)

A full-stack **Django + DRF** exam platform: timed, **auto-graded** multiple-choice
exams with **server-side anti-cheating** (one attempt, hidden answer key, enforced timer).

## What it does
- **Exams → questions → choices**, built in the admin or via the management API.
- **Start** (`@action`) creates the single allowed attempt and returns questions
  **without the answer key**.
- **Submit** (`@action`) auto-grades by comparing against `is_correct` in the DB.
- **Timer enforced on the server**: the deadline is derived from the server's start
  time, so late answers are discarded (the JS countdown also auto-submits).
- **One attempt** per student (`unique_together`), no re-submits.
- **Frontend**: exam list, live countdown, question navigation, instant results.

## Run locally
```powershell
python -m venv venv; venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed   # admin/admin, student1/student + a 3-question exam
python manage.py runserver
```
**/** exams · **/admin/** (admin/admin) · **/api/** · **/api/docs/**.

## Key endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/exams/` | list (public) |
| GET | `/api/exams/{id}/` | take view (no answer key) |
| POST | `/api/exams/{id}/start/` | begin the one attempt |
| POST | `/api/exams/{id}/submit/` | auto-grade |
| GET | `/api/exams/{id}/results/` | your score |

## Testing
```powershell
python manage.py test
```
Covers: public list, **answer key hidden**, **single-attempt rule**, **auto-grading
(full marks / zero)**, **timer enforcement discards late answers**, no double submit.

## Future scope
Question bank, randomization, proctoring, analytics, certificates.

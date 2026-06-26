# 💼 Project 4 — Job Portal (CareerHub)

A full-stack **Django + DRF** job board connecting **recruiters** (who post jobs)
with **candidates** (who apply with an uploaded resume). Heavy on **role-based access**.

## What it does
- **Profiles with roles** (recruiter / candidate), auto-created via a signal.
- **Jobs**: post (recruiters only), browse/search, filter by location & type.
- **Apply**: `@action` with **multipart resume upload**; one application per job
  (`unique_together`).
- **Role-shaped data**: candidates see only their applications; recruiters see only
  applicants to *their own* jobs (object-level checks — no IDOR).
- **Frontend**: search, recruiter posting form, candidate apply form (file upload),
  recruiter "view applicants".

## Run locally
```powershell
python -m venv venv; venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed   # admin/admin, recruiter1/recruiter, candidate1/candidate
python manage.py runserver
```
**/** job board · **/admin/** (admin/admin) · **/api/** · **/api/docs/**.

## Key endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/jobs/?search=&location=&type=` | browse (public) |
| POST | `/api/jobs/` | post a job (recruiter) |
| POST | `/api/jobs/{id}/apply/` | multipart resume (candidate) |
| GET | `/api/jobs/{id}/applicants/` | owner recruiter only |
| GET | `/api/applications/` | role-shaped (own / own jobs') |

## Testing
```powershell
python manage.py test
```
Covers: public list, **candidate can't post job (403)**, recruiter can post,
apply then **duplicate → 400**, and **recruiter sees only own applicants**.

## Future scope
Resume parsing, job alerts, messaging, skill matching.

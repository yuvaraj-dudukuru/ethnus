# 📚 Project 2 — Library Management System (Bibliotheca)

A full-stack **Django + DRF** library: browse a catalog, borrow/return books with
due dates and **atomic stock updates**, and auto-calculated **overdue fines**.

## What it does
- **Catalog**: books with authors, ISBN, total/available copies; search + filter.
- **Borrow / return** via `@action` endpoints using a race-safe `F()` stock update.
- **Fines**: computed `@property` (days late × per-day rate) charged on return.
- **Roles**: members browse & borrow; **librarians** (staff) manage books + see the
  overdue report.
- **Frontend**: live catalog, available-only filter, borrow/return buttons, "my loans".

## Run locally
```powershell
python -m venv venv; venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed         # admin/admin (librarian) + member1/member
python manage.py runserver
```
**/** catalog · **/admin/** (admin/admin) · **/api/** · **/api/docs/**.

## Key endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/books/?search=&author=&available=true` | catalog (public) |
| POST | `/api/books/{id}/issue/` | borrow a copy (member) |
| POST | `/api/books/{id}/return/` | return a copy + charge fine (member) |
| GET | `/api/issues/` | my loans (members) / all (librarian) |
| GET | `/api/issues/overdue/` | overdue report (librarian only) |

## Testing
```powershell
python manage.py test
```
Covers: public browse, issue decrements stock, **issue-beyond-stock → 400**,
return restocks, **fine calculation**, and librarian-only overdue report.

## Future scope
Reservations, e-books, barcode scanning, reading history.

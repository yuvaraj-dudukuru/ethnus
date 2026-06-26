# 📅 Project 10 — Event Management System (Evently)

A full-stack **Django + DRF** events app: organizers create events; attendees
**register with capacity limits**; organizers see their attendee lists.

## What it does
- **Events** with venue, datetime, capacity and price; search + upcoming filter.
- **Register** via `@action` inside a transaction with `select_for_update()` — the
  capacity can never be oversold, and duplicate registrations are rejected.
- **Cancel** frees a seat; **seats-left** is shown live.
- **Attendee list** is **organizer-only** (object-level check).
- **My events** for each attendee.
- **Frontend**: event cards with seats-left, register/cancel, organizer attendee view.

## Run locally
```powershell
python -m venv venv; venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed   # admin/admin, organizer1/organizer, attendee1/attendee
python manage.py runserver
```
**/** events · **/admin/** (admin/admin) · **/api/** · **/api/docs/**.

## Key endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/events/?search=&upcoming=true&venue=` | browse |
| POST | `/api/events/{id}/register/` | book a seat (capacity-enforced) |
| POST | `/api/events/{id}/cancel/` | cancel your registration |
| GET | `/api/events/{id}/attendees/` | organizer only |
| GET | `/api/registrations/` | my events |

## Testing
```powershell
python manage.py test
```
Covers: public list, register needs login, **duplicate → 400**, **capacity enforced**,
cancel frees a seat, and **attendees visible to organizer only**.

## Future scope
Ticketing/payments, QR check-in, reminders, post-event feedback.

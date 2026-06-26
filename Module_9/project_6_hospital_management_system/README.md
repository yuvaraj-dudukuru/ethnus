# 🏥 Project 6 — Hospital Management System (MediCare)

A full-stack **Django + DRF** clinic app: a doctor directory, appointment booking
that **prevents double-booking**, and **strictly access-controlled** medical records.

## What it does
- **Roles**: patient / doctor / receptionist / admin (Profile + signal).
- **Doctors**: public directory, search + filter by department & specialization.
- **Booking** via `@action`: refuses to book a doctor twice for the same slot.
- **Appointments**: role-shaped lists; patients/staff can cancel.
- **Medical records (sensitive)**: patients read **only their own**; only doctors/admins
  create. This is the headline RBAC lesson.

## Run locally
```powershell
python -m venv venv; venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed   # admin/admin, doctor1/doctor, patient1/patient, reception1/reception
python manage.py runserver
```
**/** clinic · **/admin/** (admin/admin) · **/api/** · **/api/docs/**.

## Key endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/doctors/?search=&department=&specialization=` | directory (public) |
| POST | `/api/doctors/{id}/book/` | book a slot (no double-booking) |
| POST | `/api/appointments/{id}/cancel/` | cancel (owner/staff) |
| GET/POST | `/api/records/` | read = own only; create = doctor/admin |

## Testing
```powershell
python manage.py test
```
Covers: public doctor list, **no double-booking**, appointment lifecycle,
**records private to the patient**, patient can't create a record, doctor can.

## Future scope
Prescriptions, billing, lab reports, telemedicine.

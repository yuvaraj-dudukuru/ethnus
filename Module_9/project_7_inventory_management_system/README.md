# 📦 Project 7 — Inventory Management System (StockRoom)

A full-stack **Django + DRF** inventory tool: track products, suppliers and an
**audited stock ledger**, with **atomic** stock movements and low-stock alerts.

## What it does
- **Products** with SKU, category, supplier, quantity, reorder level, price.
- **Stock in / out** via `@action` using **atomic `F()` updates** inside a transaction;
  stock can never go negative, and every change is logged as a `StockMovement`.
- **Low-stock alerts**: `low_stock` filter + endpoint (`quantity <= reorder_level`, via `F()`).
- **Audit trail**: read-only movement history.
- **Auth**: anyone can read; logged-in staff move stock; only admins edit the catalog.
- **Frontend**: live dashboard (8s polling), low-stock highlighting, CSS bar chart,
  movement feed.

## Run locally
```powershell
python -m venv venv; venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed   # admin/admin + clerk1/clerk + sample stock (2 items LOW)
python manage.py runserver
```
**/** dashboard · **/admin/** (admin/admin) · **/api/** · **/api/docs/**.

## Key endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/products/?search=&category=&low_stock=true` | catalog |
| POST | `/api/products/{id}/stock_in/` | add stock (logged) |
| POST | `/api/products/{id}/stock_out/` | remove stock (guarded, logged) |
| GET | `/api/products/low_stock/` | items needing reorder |
| GET | `/api/movements/?product=&type=` | audit log |

## Testing
```powershell
python manage.py test
```
Covers: public list, **stock-in atomicity + logging**, **stock-out can't go negative**,
**low-stock detection**, **movement audit order**, and admin-only catalog edits.

## Future scope
Purchase orders, barcode scanning, multi-warehouse, demand forecasting.

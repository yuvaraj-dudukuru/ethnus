# ✍️ Project 9 — Blog Platform (Inkwell)

A full-stack **Django + DRF** blog: publish posts (draft/published), comment, and
**like with optimistic UI**. Authors can only edit their own content.

## What it does
- **Posts** with categories, slugs, and **draft vs published** visibility.
- **Draft privacy**: drafts are visible only to their author (and admins).
- **Comments**: nested per post; any logged-in user can comment.
- **Like toggle** via `@action` — the frontend updates instantly (optimistic) then
  reconciles with the server count.
- **Author-only edit** (`IsAuthorOrReadOnly`): others get 403.
- **Frontend**: post feed, markdown preview, draft management, comment threads.

## Run locally
```powershell
python -m venv venv; venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed   # admin/admin, author1/author, reader1/reader + posts
python manage.py runserver
```
**/** blog · **/admin/** (admin/admin) · **/api/** · **/api/docs/**.

## Key endpoints
| Method | URL | Notes |
|--------|-----|-------|
| GET | `/api/posts/?search=&category=&status=` | feed (published + own drafts) |
| GET | `/api/posts/{slug}/` | detail by slug |
| POST | `/api/posts/{slug}/like/` | toggle like |
| GET/POST | `/api/comments/?post={id}` | read / add comment |

## Testing
```powershell
python manage.py test
```
Covers: **draft hidden from anon/others, visible to author**, **author-only edit (403/200)**,
anon can't comment, authed can comment, and **like toggles on/off**.

## Future scope
Rich editor, tags, RSS, follow authors, bookmarks.

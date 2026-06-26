# Module 6 Overview

Module 6 contains five separate Django-based dashboard projects. Each project is a self-contained learning app with its own `manage.py`, `requirements.txt`, database, app folder, templates, static files, and README. Together, they demonstrate how a REST API built in an earlier module can be turned into a usable front-end dashboard with AJAX, filtering, pagination, authentication, charts, and live updates.

This module is useful as a progression of front-end and API integration patterns:

- Simple CRUD dashboards
- Token-based login and protected actions
- Search, filtering, and pagination
- Optimistic UI updates
- Polling and live refresh behavior
- Chart-driven analytics and aggregate summaries

## Projects in This Folder

| Project | Folder | Main Focus |
|---|---|---|
| Project 1 | `project_1_Student_Management_Dashboard` | Student records dashboard with search, add, edit, delete, login, and pagination |
| Project 2 | `project_2_Library_Management_Dashboard` | Library dashboard with multi-filter books, issue/return flows, and staff-only views |
| Project 3 | `project_3_Blog_Management_Dashboard` | Blog dashboard with post cards, comments, publishing, and optimistic likes |
| Project 4 | `project_4_Inventory_Management_System` | Inventory dashboard with live polling, stock refresh, and admin product management |
| Project 5 | `project_5_Admin_Analytics_Dashboard` | Analytics dashboard with charts, summary cards, and date-based reporting |

## Shared Structure

Although each project solves a different problem, they all follow the same broad structure:

- `manage.py` for Django commands such as `runserver`, `migrate`, and `seed`
- `requirements.txt` for Python dependencies
- `db.sqlite3` for the local SQLite database
- A project configuration package such as `campushub`, `libraryhub`, `bloghub`, or `shophub`
- A domain app such as `students`, `library`, `blog`, or `shop`
- `templates/` for the HTML shell of the dashboard
- `static/js/dashboard.js` for the front-end logic that talks to the API

The repeated structure makes the module easy to study because once you understand one project, the others feel familiar. What changes is the interaction pattern and the type of data being presented.

## Project 1: Student Management Dashboard

Project 1 is a student administration interface. It shows a paginated student table and supports search, create, update, and delete operations. The dashboard is front-end only, and the browser communicates with the REST API in the background through AJAX requests.

Key ideas demonstrated:

- Live search as the user types
- Adding a student from a form
- Editing marks inline
- Deleting a student with confirmation
- Token-based login for write operations
- DRF pagination for page-by-page browsing

This project is the clearest example of a standard CRUD dashboard.

## Project 2: Library Management Dashboard

Project 2 turns the library API into a working circulation dashboard. It is built around books, members, and loan records. The books table supports combined filtering, while staff-only actions let a librarian issue books or return them later.

Key ideas demonstrated:

- Multi-filter search with search text, author, and availability combined into one query
- Issue-book flow with due dates and member selection
- Return-book flow from the loans view
- Staff-only access to sensitive sections such as loans and members
- Token-based authentication for protected actions

This project is the strongest example of combining multiple filters into one responsive dashboard query.

## Project 3: Blog Management Dashboard

Project 3 is a content dashboard for a blog. It presents posts as cards and lets logged-in users like posts, open comments, add new comments, and publish posts. One of the notable patterns here is the optimistic like button, which updates the interface immediately before the server response returns.

Key ideas demonstrated:

- Post cards rendered from API data
- Comment loading per post
- Comment creation without page reloads
- Optimistic UI for likes
- Author-based write access for posts
- Public reading with authenticated writing

This project is the best example of a modern, interactive feed-style interface.

## Project 4: Inventory Management System

Project 4 focuses on stock management for shop products. Instead of waiting for a manual refresh, the dashboard keeps polling the API and updates the table regularly. It also highlights stock changes visually and marks low-stock or empty rows.

Key ideas demonstrated:

- Automatic refresh through polling
- Stock diffing to update only changed rows
- Visual feedback when values increase or decrease
- Low-stock and out-of-stock highlighting
- Search and manual refresh controls
- Admin-only add, edit, and delete actions

This project is the most useful example of a dashboard that feels live even without WebSockets.

## Project 5: Admin Analytics Dashboard

Project 5 converts student data into charts and summary cards. Instead of showing row-by-row records, it aggregates data into useful metrics such as totals, averages, top scorers, department counts, monthly admissions, and pass/fail breakdowns.

Key ideas demonstrated:

- Aggregate statistics fetched from a single endpoint
- Bar, line, and doughnut charts
- Date-range filtering for analytics
- Skeleton loaders while data is loading
- Mapping API response data into Chart.js format

This project is the best example of turning raw API responses into executive-style reporting.

## What This Module Teaches

Taken together, the five projects show a clear learning path:

1. Start with a standard CRUD dashboard.
2. Add authentication and staff-only actions.
3. Improve interactivity with optimistic updates and comments.
4. Introduce live data refresh with polling and diffing.
5. Finish with analytics and chart-based reporting.

That progression is the real value of Module 6. The codebase is not just a set of unrelated apps; it is a set of front-end patterns built on top of REST APIs.

## Running Any Project

Each project can be run independently from its own folder.

Typical steps:

1. Open a terminal inside the project folder.
2. Create and activate a virtual environment.
3. Install dependencies from `requirements.txt`.
4. Run migrations.
5. Seed the database if the project provides a seed command.
6. Start the development server with `python manage.py runserver`.
7. Open the local URL shown in the terminal.

The detailed setup instructions for each app are documented in the individual README file inside that project folder.

## Folder Map

```text
Module_6/
├── README.md
├── project_1_Student_Management_Dashboard/
├── project_2_Library_Management_Dashboard/
├── project_3_Blog_Management_Dashboard/
├── project_4_Inventory_Management_System/
└── project_5_Admin_Analytics_Dashboard/
```

## Summary

Module 6 is a set of five dashboard applications that demonstrate how the same REST API style can support very different user experiences: student management, library circulation, blogging, inventory monitoring, and analytics reporting. If you are studying how Django, DRF, and JavaScript work together, this folder gives you five focused examples in one place.
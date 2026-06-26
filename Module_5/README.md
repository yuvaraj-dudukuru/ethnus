# 🚀 Module 5 — REST APIs with Django & Django REST Framework

Welcome to **Module 5**, a comprehensive collection of **five fully-functional REST API projects** built with Django and Django REST Framework (DRF). This module is designed for students learning to build professional, production-like APIs from scratch.

Each project builds on the previous ones, introducing new concepts and best practices. Every code file is heavily commented, making it easy to understand exactly what each line does.

---

## 📚 Table of Contents
1. [Module Overview](#-module-overview)
2. [Project Overview (Quick Reference)](#-project-overview-quick-reference)
3. [Individual Projects](#-individual-projects)
4. [Common Setup Instructions](#-common-setup-instructions)
5. [Key Learning Outcomes](#-key-learning-outcomes)
6. [Tech Stack](#-tech-stack)
7. [Contributing & Support](#-contributing--support)

---

## 🎯 Module Overview

**Module 5** teaches you how to build **REST APIs** — the backbone of modern web and mobile applications. Instead of writing HTML pages, you build JSON endpoints that other apps (websites, mobile apps, scripts) call over HTTP.

This module follows a **progressive learning path**:
- **Projects 1–2** teach the fundamentals: authentication, permissions, filtering, pagination.
- **Projects 3–4** add intermediate skills: custom actions, file uploads, owner-scoped data.
- **Project 5** brings it all together with role-based access control and realistic workflows.

**Why five projects?** Because building APIs is a skill that requires **practice**. Each project extends your toolkit without starting from zero. You'll see common patterns recurring with slight variations, cementing your understanding.

---

## 📋 Project Overview (Quick Reference)

| # | Project | Purpose | Key Skills | Models |
|---|---------|---------|-----------|--------|
| 1️⃣ | [CampusHub](#-project-1--student-management-rest-api-campushub) | Manage college students | Token auth, permissions, search/filter/pagination, throttling | Student, Department |
| 2️⃣ | [LibraryHub](#-project-2--library-management-rest-api-libraryhub) | Manage library borrowing | Custom actions, computed fields, reports | Book, Author, Member, Issue |
| 3️⃣ | [BlogHub](#-project-3--blog-rest-api-bloghub) | Power a blog platform | Owner-only edits, slug URLs, two-serializer pattern, nested routes | Post, Category, Comment, User |
| 4️⃣ | [ShopHub](#-project-4--e-commerce-rest-api-shophub) | Run an online shop | Database cart (not session), transactional checkout, price snapshots, cursor pagination | Product, Category, Cart, CartItem, Order, OrderItem |
| 5️⃣ | [JobHub](#-project-5--job-portal-rest-api-jobjub) | Job board with roles | File uploads, role-based permissions, per-role querysets, status transitions | Job, Application, User, Profile |

---

## 🔍 Individual Projects

### 🎓 Project 1 — Student Management REST API (CampusHub)

**What:** A REST API for managing college students and departments.

**Learning Goals:**
- Build your first API with Django REST Framework
- Understand token-based authentication
- Learn permission classes and throttling
- Master search, filtering, and ordering
- Implement pagination

**Key Endpoints:**
- `POST /api/login/` — Get a token
- `GET /api/students/` — List students (with search/filter/page)
- `POST /api/students/` — Create a student (logged-in only)
- `PUT/PATCH /api/students/{id}/` — Update a student
- `DELETE /api/students/{id}/` — Delete a student (admin only)
- `GET /api/students/toppers/` — Top 5 active students

**Models:** Student, Department

**Quick Start:**
```bash
cd Project_1_Student_Management_REST_API
python manage.py migrate
python manage.py seed  # Create sample data
python manage.py runserver
# Visit http://127.0.0.1:8000/api/
# Login: admin / admin
```

**File Structure:**
```
students/
├── models.py          # Student & Department models
├── serializers.py     # Validation & JSON conversion
├── api_views.py       # API endpoints (viewsets, actions)
├── filters.py         # Search & filter logic
└── permissions.py     # Who can do what
```

---

### 📚 Project 2 — Library Management REST API (LibraryHub)

**What:** A REST API for managing books, authors, members, and borrowing records.

**Learning Goals:**
- Implement **custom business actions** (`borrow`, `return_book`)
- Add **computed fields** to serializers (e.g., book availability, late fines)
- Build **reports** (e.g., overdue books + total fine)
- Use **group-based permissions** (Librarians group)
- Handle **stock tracking**

**Key Endpoints:**
- `GET /api/books/` — List books (with availability)
- `POST /api/books/{id}/issue/` — **Borrow a book** (stock-checked)
- `POST /api/issues/{id}/return_book/` — **Return a borrowed book**
- `GET /api/reports/overdue/` — Overdue books + fines owed (staff only)
- `GET /api/members/` — List members (staff only)

**Models:** Book, Author, Member, Issue

**Quick Start:**
```bash
cd Project_2_Library_Management_API
python manage.py migrate
python manage.py seed
python manage.py runserver
# Login: admin / admin  or  librarian / librarian
```

**What's New:**
- **Viewset actions** — Actions that sit on models (e.g., `/books/1/issue/`)
- **Computed fields** — Fields calculated on-the-fly (e.g., `is_available`, `fine_owed`)
- **Group permissions** — The "Librarians" group can edit books; others can't

---

### ✍️ Project 3 — Blog REST API (BlogHub)

**What:** A REST API powering a blog with posts, categories, and comments.

**Learning Goals:**
- Implement **owner-only permissions** (`IsOwnerOrReadOnly`)
- Use **slug-based URLs** (e.g., `/posts/django-tips/` instead of `/posts/7/`)
- Apply the **two-serializer pattern** — slim list view, rich detail view
- Handle **nested routes** — `/posts/{slug}/comments/`
- Add **per-endpoint throttling** (spam protection)

**Key Endpoints:**
- `GET /api/posts/` — Public posts (published only)
- `POST /api/posts/` — Create a post (you're the author)
- `PUT/PATCH /api/posts/{slug}/` — Edit your own posts (owner only)
- `DELETE /api/posts/{slug}/` — Delete your own posts (owner only)
- `GET /api/my-posts/` — Your drafts + published posts (logged-in only)
- `GET /api/posts/{slug}/comments/` — Comments on a post
- `POST /api/posts/{slug}/comments/` — Add a comment (30/hour limit)

**Models:** Post, Category, Comment, User

**Quick Start:**
```bash
cd Project_3_Blog_REST_API
python manage.py migrate
python manage.py seed
python manage.py runserver
# Create a post, then try updating it (only you can)
```

**What's New:**
- **Slug URLs** — Human-readable URLs that also serve as lookups
- **Draft/Publish** — Posts can be hidden (draft) or public
- **Author stamping** — Server auto-stamps the logged-in user as the author
- **The two-serializer pattern** — `PostListSerializer` (simple) vs. `PostDetailSerializer` (rich)

---

### 🛒 Project 4 — E-Commerce REST API (ShopHub)

**What:** A REST API powering an online shop with a product catalog, cart, and checkout.

**Learning Goals:**
- Understand why **carts must be database rows** (not session data) in stateless APIs
- Build a **transactional checkout** (all-or-nothing)
- Implement **cursor pagination** (better for live, changing catalogs)
- Take a **price snapshot** (orders freeze prices, so history is correct)
- Master **owner-scoped queryset** (you only see your own cart/orders)

**Key Endpoints:**
- `GET /api/products/` — Browse products (cursor-paginated)
- `POST /api/products/` — Add a product (admin/staff only)
- `GET /api/cart/` — View **your** cart
- `POST /api/cart/items/` — Add to cart (e.g., `{product: 1, qty: 2}`)
- `DELETE /api/cart/items/` — Remove from cart
- `POST /api/orders/` — **CHECKOUT** — make an order from your cart
- `GET /api/orders/` — List **your** orders

**Models:** Product, Category, Cart, CartItem, Order, OrderItem

**Quick Start:**
```bash
cd Project_4_E_Commerce_API
python manage.py migrate
python manage.py seed
python manage.py runserver
# Browse products, add to cart, checkout
```

**What's New:**
- **Database cart** — Cart is real rows keyed to the user (not session data)
- **Transactional checkout** — `POST /api/orders/` atomically: creates the order, empties the cart, or fails completely
- **Price snapshot** — Each order line stores `price_at_purchase`; later price changes don't rewrite history
- **Cursor pagination** — For the catalog, you get `next`/`previous` links (better for changing data)
- **Owner-scoped** — `/api/cart/` and `/api/orders/` are always your own; guessing another user's ID gives 404

---

### 💼 Project 5 — Job Portal REST API (JobHub)

**What:** A REST API powering a job board with recruiters (who post jobs) and candidates (who apply).

**Learning Goals:**
- Implement **role-based access control** end-to-end
- Handle **file uploads** through the API (`multipart/form-data`)
- Use **per-role querysets** — same endpoint, different data depending on role
- Build **status-transition actions** (recruiter accepts/rejects applicants)
- Protect against data leaks between roles

**Key Endpoints:**
- `POST /api/register/` — Sign up with a role (`R`=recruiter, `C`=candidate)
- `POST /api/login/` — Log in → token
- `GET /api/jobs/` — List jobs (anyone)
- `POST /api/jobs/` — Post a job (recruiters only)
- `POST /api/jobs/{id}/apply/` — **Apply with resume file** (candidates only)
- `GET /api/applications/` — Recruiter sees their applicants; candidate sees own applications
- `PATCH /api/applications/{id}/set_status/` — Accept/reject an applicant (recruiter only)

**Models:** Job, Application, User, Profile

**Quick Start:**
```bash
cd Project_5_Job_Portal_API
python manage.py migrate
python manage.py seed
python manage.py runserver
# Register as a recruiter, post a job
# Register as a candidate, apply with a resume file
```

**What's New:**
- **Roles** — Every user is a Recruiter or Candidate (stored in Profile)
- **Role-based permissions** — Decorators like `@IsRecruiter` or `@IsCandidate`
- **File uploads** — Resume upload via `multipart/form-data` (the only non-JSON endpoint)
- **Per-role querysets** — `/api/applications/` returns different data based on your role
- **Signals** — Automatically create a Profile when a User is created

---

## 🛠️ Common Setup Instructions

All five projects follow the same setup pattern. Here's how to run **any** of them:

### 1. Navigate to the Project
```bash
cd Project_X_Name_Of_Project
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. (Optional) Seed Sample Data
```bash
python manage.py seed
```
This command creates sample users, posts, products, jobs, etc., so you can immediately test the API.

### 6. Start the Server
```bash
python manage.py runserver
```

### 7. Access the API
- **Interactive API docs:** http://127.0.0.1:8000/api/
- **Admin panel:** http://127.0.0.1:8000/admin/
  - Default login: `admin` / `admin`

### 8. Stop the Server
```bash
Ctrl+C
```

---

## 📚 Key Learning Outcomes

By completing all five projects, you will master:

### **Authentication & Authorization**
- Token-based authentication
- Permission classes (`IsAuthenticated`, `IsAdminUser`, `IsOwnerOrReadOnly`)
- Group-based permissions
- Role-based access control (RBAC)

### **API Design**
- RESTful principles
- Proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Meaningful status codes and error messages
- Pagination (limit-offset, cursor-based)
- Filtering, searching, and ordering

### **Serializers & Validation**
- Basic serializers
- Computed fields
- Nested serializers
- Custom validation
- Two-serializer patterns (list vs. detail)

### **Viewsets & Actions**
- `ModelViewSet` (auto-generates CRUD endpoints)
- Custom actions (`@action`)
- Business logic endpoints (e.g., `/borrow/`, `/apply/`)

### **Advanced Patterns**
- File uploads via the API
- Transactional operations (checkout)
- Price/data snapshots
- Per-role querysets
- Owner-scoped data (IDOR prevention)

### **Real-World Considerations**
- Throttling (rate-limiting)
- Proper permissions to prevent data leaks
- Automated user stamping
- Slug-based URLs
- Signal handlers for side effects

---

## 🔧 Tech Stack

All projects use the same core stack:

| Component | Version/Tool | Purpose |
|-----------|--------------|---------|
| **Language** | Python 3.10+ | Server-side language |
| **Framework** | Django 4.2+ | Web framework |
| **API Layer** | Django REST Framework (DRF) 3.14+ | REST API tools |
| **Database** | SQLite | Lightweight, file-based (no server needed) |
| **Admin Panel** | Django Admin | Built-in data management UI |

### Optional Tools:
- **Postman** — Test API endpoints visually
- **cURL** — Command-line API testing
- **Thunder Client** (VS Code extension) — API testing in the editor

---

## 📖 How to Use This Module

### For Learners
1. **Start with Project 1** — Get comfortable with basic API building.
2. **Move sequentially** — Each project builds on the previous one.
3. **Read the code** — Every file is heavily commented. Take time to understand *why* each line is there.
4. **Experiment** — Modify the code, add fields, break things, and fix them.
5. **Build your own** — Use what you've learned to build a 6th project (e.g., a movie review API, a task manager, etc.).

### For Instructors / Reviewers
- Use each project as a **reference implementation** for the concepts.
- All code is **intentionally verbose** — prefer clarity over brevity.
- Each project has a **separate README** with detailed API docs and setup steps.
- All projects use **SQLite** — no database server needed.
- The **seed command** populates realistic sample data for testing.

---

## 🤝 Contributing & Support

### Troubleshooting Common Issues

**Database errors after making changes to models?**
```bash
# Backup your current database
mv db.sqlite3 db.sqlite3.bak
# Re-create from migrations
python manage.py migrate
python manage.py seed
```

**Dependencies missing?**
```bash
pip install -r requirements.txt --force-reinstall
```

**Port 8000 already in use?**
```bash
python manage.py runserver 8001
```

**Permission denied running migrations?**
```bash
# On Windows, make sure you're in the project directory
# and the virtual environment is activated
python manage.py migrate
```

---

## 📝 Project Structure (Overview)

Each project follows this pattern:

```
Project_N_Name/
├── README.md              # Project-specific documentation
├── manage.py              # Django management script
├── db.sqlite3             # SQLite database (created after first migration)
├── requirements.txt       # Python dependencies
├── ProjectName/           # Main Django project folder
│   ├── settings.py        # Configuration
│   ├── urls.py            # Root URL routing
│   ├── asgi.py            # ASGI (websocket support)
│   ├── wsgi.py            # WSGI (production deployment)
│   └── pagination.py      # Custom pagination classes
├── app_name/              # Django app folder (e.g., students, books, posts)
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers (JSON validation)
│   ├── api_views.py       # Viewsets & API endpoints
│   ├── permissions.py     # Permission classes
│   ├── filters.py         # Filtering & search logic
│   ├── tests.py           # Unit tests
│   ├── admin.py           # Admin panel configuration
│   └── migrations/        # Database migration files
└── media/                 # User-uploaded files (if applicable)
```

---

## 🎓 Next Steps

After completing all five projects:

1. **Build your own API** — Pick a domain you're interested in and build a full API from scratch.
2. **Deploy to production** — Learn to deploy on Heroku, PythonAnywhere, or AWS.
3. **Add frontend** — Build a React or Vue.js frontend that calls your API.
4. **Add caching** — Learn Redis and implement caching for performance.
5. **Advanced security** — Study JWT tokens, CORS, SQL injection prevention, etc.

---

## 📞 Questions?

Refer to the **individual project README files** for detailed docs, API contracts, and troubleshooting steps specific to each project.

**Happy coding! 🚀**

---

**Module 5 — Master REST APIs with Django & DRF**
*Built for students. By students. With ❤️.*

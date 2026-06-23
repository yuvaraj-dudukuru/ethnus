# Project 2 — Student Profile Website (Bootstrap Basics)

A clean **student profile page** for *Vikram Rao*. This project's whole purpose is
to introduce **Bootstrap** — and to show how much you can build **without writing
a single line of your own CSS** (that's why the file is named `no_css.html`).

---

## 📁 Files

| File | Role |
|------|------|
| `no_css.html` | The entire page — structure **and** styling come from Bootstrap classes (fully commented). |
| `images/` | Folder for the profile photo (`photo.jpg`). |

> Note: this project references `images/photo.jpg` and `files/resume.pdf`. Add
> your own files with those names/paths to see them appear.

---

## 🤔 What is Bootstrap?

**Bootstrap** is the world's most popular **CSS framework** — a huge, ready-made
stylesheet full of pre-designed "classes". Instead of writing CSS yourself, you
add Bootstrap's class names to your HTML elements and they instantly look styled
and professional.

It is loaded with a single line in the `<head>`:
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
```
That link points to a **CDN** (Content Delivery Network) — a fast online file
host — so there's nothing to download or install.

---

## 🖼️ What the page contains

1. **Responsive navbar** — collapses into a "hamburger" menu on small screens.
2. **Profile header** — circular photo, name, info, coloured badges, and buttons.
3. **Personal Information** — a striped, bordered table.
4. **Semester Performance** — a hover-highlighted, responsive marks table.
5. **Footer** — social icons and a copyright line.

---

## 🧠 Bootstrap concepts demonstrated

### The 12-column Grid System
Bootstrap divides each **`row`** into **12 columns**. You choose how many columns
an element spans using `col-*` classes:
```html
<div class="row">
  <div class="col-md-4">...</div>   <!-- one-third (4 of 12) on medium+ screens -->
  <div class="col-md-8">...</div>   <!-- two-thirds (8 of 12) -->
</div>
```
On smaller screens the columns automatically **stack vertically** — that's
responsive design for free.

### Component & utility classes used here
| Class | What it does |
|-------|--------------|
| `navbar`, `navbar-expand-md` | A responsive navigation bar that collapses on small screens. |
| `container` | Centres content with sensible side margins. |
| `btn`, `btn-primary`, `btn-outline-primary` | Pre-styled buttons (filled & outlined). |
| `badge`, `bg-success`, `bg-info` | Small coloured label pills. |
| `table`, `table-striped`, `table-hover`, `table-bordered` | Instantly styled tables. |
| `rounded-circle`, `shadow`, `img-fluid` | Circular, shadowed, responsive image. |
| `text-center`, `text-muted`, `fw-bold`, `fs-5` | Quick text alignment/colour/size helpers. |
| `my-5`, `mb-3`, `mt-3`, `g-4` | **Spacing utilities** — margins, padding and grid gaps. |

### Bootstrap Icons
A matching free icon font. Loaded once, then used like:
```html
<i class="bi bi-download"></i>   <!-- a download icon -->
<i class="bi bi-github"></i>     <!-- a GitHub icon -->
```

### Bootstrap JavaScript
The script at the bottom of `<body>` powers the **interactive** parts — here, the
collapsing hamburger menu:
```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

---

## ▶️ How to view it

1. **Double-click `no_css.html`** to open it in your browser.
2. Shrink the window narrow to watch the navbar collapse into a hamburger menu
   and the columns stack vertically.

---

## ✅ What you should take away

- A framework like Bootstrap lets beginners build clean, **responsive** pages
  fast, using only HTML classes.
- The **grid system** (`row` + `col-*`) is the foundation of every Bootstrap layout.
- **Utility classes** (spacing, colours, text) handle the small tweaks you'd
  otherwise write CSS for.

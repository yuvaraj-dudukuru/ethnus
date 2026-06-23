# Project 6 — Responsive Business Website

The home page of a fictional data-consulting company, **Nimbus**. This is the
**capstone** project of Module 3: it's structured like a **real multi-page
business website**, with a shared navbar and footer designed to be reused across
several pages, a hero, a stats bar, and a full contact section.

---

## 📁 Files

| File | Role |
|------|------|
| `index.html` | The home page (fully commented). |
| `style.css` | Background-image hero, card hover effect, footer link colours (fully commented). |

> The navbar links to `services.html` and `team.html`. Those pages aren't
> included here — the project is intentionally set up so you can **create them
> by copying the shared navbar/footer**, which is the whole lesson of this build.

---

## 🖼️ What the page contains

1. **Shared navbar** — links to *other pages* of the site, with the current page
   marked `active`.
2. **Hero** — a full-width background photo with a dark overlay and a CTA button.
3. **Stats bar** — four key numbers (clients, experience, experts, rating).
4. **Contact section** — a form on the left, contact details + an embedded map
   on the right.
5. **Shared footer** — copyright + a link, meant to appear on every page.

---

## ⭐ The key new idea: thinking in **multiple pages**

Every project before this was a single page. A real website is usually **many
pages that share a common look**. This project teaches that mindset:

- The navbar links go to **separate `.html` files** (`services.html`,
  `team.html`) instead of `#section` anchors on the same page:
  ```html
  <a class="nav-link active" href="index.html">Home</a>
  <a class="nav-link" href="services.html">Services</a>
  <a class="nav-link" href="team.html">Team</a>
  ```
- The `active` class highlights whichever page you're currently on.
- The **navbar and footer are marked "SHARED"** in the comments — the idea is to
  **copy them onto every page** so the whole site feels consistent. (In bigger
  projects, tools or frameworks do this automatically, but copying is the
  beginner-friendly first step.)

---

## 🧠 Concepts demonstrated

### New / spotlighted here
| Concept | Where it appears |
|---------|------------------|
| **Multi-page navigation** | Navbar links to `services.html`, `team.html`. |
| **`active` nav state** | Highlights the current page in the menu. |
| **Shared layout pieces** | A reusable navbar + footer pattern. |
| **`<textarea>`** | The multi-line "Message" field in the contact form. |
| **`<aside>` semantic tag** | Side content (contact details next to the form). |
| **Background-image hero with overlay** | Dark gradient over an Unsplash photo for readable text. |
| **Responsive stats** | `col-6 col-md-3` → 2 per row on phones, 4 on desktop. |

### Reinforced from earlier projects
- Bootstrap grid, responsive navbar, forms, and Bootstrap Icons.
- Embedded Google Map via `<iframe>`.
- A thin custom `style.css` layered over Bootstrap.

---

## ▶️ How to view it

1. **Double-click `index.html`** to open it in your browser.
2. Shrink the window to watch the navbar collapse and the stats/contact columns
   re-stack.
3. *(Optional, to extend it):* create `services.html` and `team.html` by copying
   this file, keeping the same navbar/footer, and changing the middle content —
   that's exactly the multi-page workflow this project is teaching.

---

## ✅ What you should take away

- Real websites are **collections of pages** that share a consistent header and
  footer.
- The `active` class and consistent navigation help users know where they are.
- By Project 6 you've combined **everything** — layout, components, forms, icons,
  maps, animations, and responsive design — into a professional-looking site.

# Project 3 — Restaurant Landing Page (Bootstrap + Custom CSS)

A polished, full-screen **landing page** for a fictional Indian restaurant,
**Spice Route**. This project is a step up from Project 2: it **combines
Bootstrap with a custom `style.css`** to create a unique brand identity, and it
introduces interactive components like a **pop-up booking modal**.

---

## 📁 Files

| File / Folder | Role |
|---------------|------|
| `Restaurant_Landing_Page.html` | The page structure & content (fully commented). |
| `style.css` | Custom brand styling layered on top of Bootstrap (fully commented). |
| `images/` | Dish & interior photos: `biryani.jpg`, `paneer.jpg`, `dosa.jpg`, `hero.jpg`. |

---

## 🖼️ What the page contains

1. **Sticky navbar** with a "Book a Table" button that opens a pop-up.
2. **Full-screen hero** — a background photo with a dark overlay and white text.
3. **Signature Dishes** — three responsive dish cards with prices and hover zoom.
4. **Our Story** — an image + text section with a rating badge.
5. **Footer** — opening hours, address, and an **embedded Google Map**.
6. **Booking Modal** — a pop-up form (name, date, guest count).

---

## ⭐ The key new idea: Bootstrap **+** custom CSS together

Project 2 used only Bootstrap. Here we get the **best of both worlds**:

- **Bootstrap** provides the heavy lifting — grid, navbar, cards, modal, forms.
- **`style.css`** adds the personality — the warm orange theme, elegant
  *Playfair Display* font, the background-image hero, and the hover animations.

This works because of CSS **order**: our stylesheet is linked **after** Bootstrap,
so where both define the same thing, **ours wins** (sometimes nudged along with
`!important`).

```html
<link href=".../bootstrap.min.css" rel="stylesheet">  <!-- loaded first  -->
<link rel="stylesheet" href="style.css">               <!-- overrides it  -->
```

---

## 🧠 Concepts demonstrated

### New in this project
| Concept | Where it appears |
|---------|------------------|
| **Modal (pop-up dialog)** | The "Book a Table" form. Opened by `data-bs-toggle="modal"` + `data-bs-target="#bookModal"`. |
| **Forms & inputs** | `type="text"`, `type="date"`, `type="number"`, with `required`, `min`, `max`. |
| **`<label for="...">`** | Connects a label to its input (better accessibility). |
| **Background-image hero** | A photo + dark gradient overlay set in CSS so white text stays readable. |
| **Embedded map** | A Google Map placed with an `<iframe>`. |
| **`@import` Google Fonts** | Loading fonts from inside the CSS file. |
| **Accessibility (`aria-*`)** | `aria-label`, `aria-expanded` help screen-reader users. |
| **SEO `<meta name="description">`** | The summary shown in Google search results. |
| **`loading="lazy"` images** | Images load only when scrolled near — faster page load. |

### Reinforced from earlier projects
- Bootstrap **grid** (`row` + `col-12 col-md-6 col-lg-4`) for responsive cards.
- **CSS variables**, **transitions**, **`:hover`** and **`:focus`** effects.
- Gradients, shadows, and `transform: translateY()` lift animations.

---

## ▶️ How to view it

1. Make sure the `images/` folder (with `hero.jpg`, `biryani.jpg`, etc.) sits
   next to the HTML file — the hero background and dish photos rely on them.
2. **Double-click `Restaurant_Landing_Page.html`** to open it in your browser.
3. Click **"Book a Table"** to see the modal pop up.
4. Shrink the window to watch the dish cards re-stack (3 → 2 → 1 per row).

---

## ✅ What you should take away

- Frameworks and custom CSS are **complementary**, not either/or.
- Interactive components (modals) come "for free" with Bootstrap's JavaScript —
  you only need the right `data-bs-*` attributes.
- Small details — overlays for readability, lazy loading, `aria-*` labels, an
  SEO description — are what separate a basic page from a professional one.

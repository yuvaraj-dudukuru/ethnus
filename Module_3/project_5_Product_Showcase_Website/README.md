# Project 5 — Product Showcase Website

A sleek, single-product **sales page** for fictional wireless earbuds, **AuraBuds
Pro**. This project recreates the layout of a real e-commerce product landing
page: a hero with a floating product image, a features strip, **tiered pricing**,
a specs table, customer reviews, and a "Buy" pop-up.

---

## 📁 Files

| File / Folder | Role |
|---------------|------|
| `index.html` | The full product page (fully commented). |
| `style.css` | The floating-image animation + featured-card scaling (fully commented). |
| `images/` | Product image (`buds.png`). |

---

## 🖼️ What the page contains

1. **Hero** — product name, tagline, two buttons, and a gently **floating** image.
2. **Features strip** — three icon-led highlights (battery, ANC, water resistance).
3. **Pricing** — three bundles (Basic / Pro / Max), with **Pro** highlighted as
   "Most Popular".
4. **Specifications** — a clean striped table of technical details.
5. **Customer Reviews** — cards with **star ratings** (including a half-star).
6. **Buy Modal** — a shared pop-up with quantity + colour selectors.
7. **Footer** — copyright line.

---

## ⭐ The key new idea: a polished e-commerce layout

This project doesn't introduce a brand-new technology — instead it shows how to
**combine everything so far into a convincing product page**, with attention to
the small visual touches shoppers expect:

- A **floating product image** (a custom CSS `@keyframes` animation).
- A **highlighted "Most Popular" tier** using `transform: scale()` plus a badge
  positioned right on the card's edge.
- **Star ratings** built purely from Bootstrap Icons (`bi-star-fill`,
  `bi-star-half`).

### Spotlighting the featured pricing card
```css
.featured { transform: scale(1.05); }            /* make the Pro card bigger */
@media (max-width: 767px) { .featured { transform: none; } }  /* but not on phones */
```
That media query is a nice example of a **responsive tweak** — an effect that
looks good on desktop but would look odd on a narrow phone, so it's switched off.

---

## 🧠 Concepts demonstrated

### New / spotlighted here
| Concept | Where it appears |
|---------|------------------|
| **Pricing tiers** | Three cards, one promoted with `border-primary` + `shadow` + `featured`. |
| **Absolute-positioned badge** | "Most Popular" pinned to the card edge with `position-absolute top-0 start-50 translate-middle`. |
| **Icon star ratings** | `bi-star-fill` and `bi-star-half` styled gold via `text-warning`. |
| **Floating image animation** | A custom `@keyframes floaty` that bobs the image up and down. |
| **`scope="row"` table headers** | Accessibility — tells screen readers which header labels each row. |
| **Shared modal** | Every "Buy" button opens the same `#buyModal`. |

### Reinforced from earlier projects
- Bootstrap grid, cards, badges, buttons, tables, and modal.
- Bootstrap Icons.
- A thin custom `style.css` layered over Bootstrap.

---

## ▶️ How to view it

1. Make sure `images/buds.png` exists next to `index.html`.
2. **Double-click `index.html`** to open it in your browser.
3. Watch the product image **float**, then click any **Buy** button to open the
   purchase modal. Resize the window to see the layout adapt.

---

## ✅ What you should take away

- A great product page is mostly about **combining familiar pieces** thoughtfully.
- Small animations and a highlighted "best value" tier are powerful, low-effort
  ways to guide a shopper's eye.
- One reusable modal can serve many buttons.

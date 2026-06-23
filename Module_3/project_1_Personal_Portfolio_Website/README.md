# Project 1 — Personal Portfolio Website

A modern, single-page **personal portfolio** built from scratch with **pure HTML
and CSS** — no frameworks. It showcases a developer named *Asha Verma* and is the
first project of Module 3, designed to teach the fundamentals of how a web page
is structured and styled.

The standout feature is its **glassmorphism** design: frosted-glass cards floating
over a dark background with soft, animated colour blobs.

---

## 📁 Files

| File | Role |
|------|------|
| `index.html` | The page **structure** and content (fully commented). |
| `style.css` | The page **appearance** — colours, layout, animation (fully commented). |

---

## 🖼️ What the page contains

1. **Navbar** — a sticky top bar with the logo and smooth-scroll links.
2. **Hero** — the big welcome banner with name, tagline and two buttons.
3. **About** — a glass card with a photo and a short bio.
4. **Skills** — a responsive grid of skill cards (HTML, CSS, Python, …).
5. **Projects** — cards describing featured projects.
6. **Footer / Contact** — email + GitHub links and a copyright line.

---

## 🧠 Beginner concepts demonstrated

### HTML (structure)
| Concept | Where / why it's used |
|---------|----------------------|
| `<!DOCTYPE html>` & `<head>`/`<body>` | The standard skeleton of every web page. |
| Semantic tags (`<header>`, `<section>`, `<article>`, `<footer>`) | Tags whose **names describe their purpose**, which helps accessibility and SEO. |
| `id` + `href="#id"` | Click a nav link → smoothly jump to that section on the page. |
| `<img src alt>` | Display images; `alt` is fallback text for screen readers. |
| Google Fonts `<link>` | Load custom fonts ("Inter" & "Outfit"). |

### CSS (appearance)
| Concept | What it teaches |
|---------|-----------------|
| **CSS variables** (`:root { --primary: ... }`) | Define a colour once, reuse it everywhere. |
| **Flexbox** (`display: flex`) | Arrange items in a row/column and align them. |
| **CSS Grid** (`display: grid`) | Build responsive multi-column layouts. |
| **`backdrop-filter: blur()`** | The frosted-glass (glassmorphism) effect. |
| **Gradients & `background-clip: text`** | Multi-colour buttons and gradient text. |
| **Transitions & `:hover`** | Smooth hover effects (cards lift, links underline). |
| **`@keyframes` animations** | The floating background blobs and fade-in hero. |
| **Media queries** (`@media`) | Make the layout **responsive** on phones/tablets. |

---

## ▶️ How to view it

No installation or build step is needed — it's plain HTML/CSS.

1. Open the project folder.
2. **Double-click `index.html`** — it opens in your default web browser.
3. Resize the browser window to watch the **responsive** layout adapt.

> 💡 Tip: For live-reloading while editing, use the **Live Server** extension in
> VS Code (right-click `index.html` → *Open with Live Server*).

---

## 🎨 Customising it

- Change the colour theme by editing the variables in the `:root { … }` block of
  `style.css`.
- Replace the photo by changing the `src` of the `<img>` in the About section.
- Edit the text in `index.html` to make it your own portfolio.

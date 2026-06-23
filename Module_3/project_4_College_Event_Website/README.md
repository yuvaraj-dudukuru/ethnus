# Project 4 — College Event Website

A landing page for a fictional national-level college tech fest, **TechNova
2026**. This project introduces **interactivity with JavaScript** for the first
time: a registration form that **validates the user's input** before it can be
submitted. It also covers advanced HTML tables and an animated gradient banner.

---

## 📁 Files

| File / Folder | Role |
|---------------|------|
| `index.html` | The page structure, including the validation script (fully commented). |
| `style.css` | Just the animated gradient hero + speaker-image sizing (fully commented). |
| `images/` | Speaker headshot (`sp1.jpg`) and sponsor logos (`logo1–3.jpg`). |

---

## 🖼️ What the page contains

1. **Animated hero** — a colour-shifting gradient banner with a Register button.
2. **Event Schedule** — a table that uses **merged cells** (`rowspan`) to group
   sessions under "Day 1" and "Day 2".
3. **Speakers** — responsive cards (1 / 2 / 4 per row depending on screen width).
4. **Registration form** — with **live validation** (name length, valid email,
   event must be chosen).
5. **FAQ** — built with a semantic description list (`<dl>`), plus sponsor logos.

---

## ⭐ The key new idea: JavaScript form validation

HTML builds the structure and CSS styles it — but **JavaScript adds behaviour**.
Here, a small script stops the form from submitting if any field is invalid, and
turns on Bootstrap's red/green highlighting.

### How it works (plain English)
```js
(function () {
  'use strict'
  var forms = document.querySelectorAll('.needs-validation')  // find the form(s)
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {        // when submitted...
      if (!form.checkValidity()) {     // ...if any field breaks its rules
        event.preventDefault()         // block the submission
        event.stopPropagation()
      }
      form.classList.add('was-validated')  // show the red/green feedback
    }, false)
  })
})()
```

The HTML side cooperates using:
- `class="needs-validation"` + `novalidate` on the `<form>`,
- validation rules on inputs: `required`, `minlength="3"`, `type="email"`,
- `<div class="invalid-feedback">` messages that appear only when a field fails.

---

## 🧠 Concepts demonstrated

### New in this project
| Concept | Where it appears |
|---------|------------------|
| **JavaScript event handling** | `addEventListener('submit', ...)` on the form. |
| **`checkValidity()` / `preventDefault()`** | Block submission when input is invalid. |
| **HTML5 form validation attributes** | `required`, `minlength`, `type="email"`. |
| **Table `rowspan`** | Merging the "Day 1"/"Day 2" cells across multiple rows. |
| **`<select>` dropdown** | Choosing which event to register for. |
| **Description list `<dl>` / `<dt>` / `<dd>`** | The FAQ section (term → answer). |
| **Animated CSS gradient** | `background-size: 200%` + a `@keyframes` shift. |
| **`row-cols-*`** | Control cards-per-row responsively without writing column classes on each card. |

### Reinforced from earlier projects
- Bootstrap layout utilities (`container`, `d-flex`, spacing helpers).
- Bootstrap cards, badges, buttons and responsive tables.
- An external `style.css` layered on top of Bootstrap.

---

## ▶️ How to view it

1. Make sure the `images/` folder sits next to `index.html`.
2. **Double-click `index.html`** to open it in your browser.
3. Scroll to **Register** and click **Submit Registration** with empty fields —
   you'll see the validation messages and red highlights appear. Fill the fields
   correctly and the warnings turn green.

---

## ✅ What you should take away

- The three languages of the front end work together: **HTML** (structure),
  **CSS** (looks), **JavaScript** (behaviour).
- You don't always need much JS — a tiny, well-placed snippet can power real
  interactivity like form validation.
- HTML tables can express complex layouts using `rowspan`/`colspan`.

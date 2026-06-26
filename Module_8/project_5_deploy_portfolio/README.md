# 🔴 Project 5 — Deploy the Portfolio Website (the one that matters for jobs)

A fast, static portfolio that sits at the **top of your resume** and **links to
every other deployed project** in Module 8. Simplest stack (HTML/CSS/JS), so the
focus is on the things recruiters notice: a **custom domain**, **HTTPS**, a
**polished 404**, **fast compressed load**, and **SEO meta tags** (Module 3).

> **Live URL (after you deploy):** `https://yourname.dev`
> (or `https://<your-username>.github.io/portfolio/`)

---

## 🔑 1. Credentials & IDs

This is a **static site — there is no database, no login, and no password.** The
only identifiers you configure are *your own*:

| Item | Where to set it | Current placeholder |
|------|-----------------|---------------------|
| Contact email | `index.html` (mailto link) | `nihalkoona7@gmail.com` |
| GitHub URL | `index.html` (Contact) | `https://github.com/your-username` |
| LinkedIn URL | `index.html` (Contact) | `https://www.linkedin.com/in/your-handle` |
| Custom domain | `CNAME`, `index.html` canonical/OG, `robots.txt`, `sitemap.xml` | `yourname.dev` |
| Live project URLs | `index.html` `data-url="…"` on each `.card` | the four `*.onrender.com` URLs |

> 🔁 After deploying Projects 1–4, paste their real `.onrender.com` URLs into the
> four project cards' `data-url` attributes so the cards open the live apps.

---

## 📁 2. What's in here

| File | Purpose |
|------|---------|
| `index.html` | The whole one-page site (hero, projects, journey, about, contact). |
| `styles.css` | Dark theme, responsive grid, gradient accent. |
| `script.js` | Footer year + open project cards in new tabs. |
| `404.html` | Polished not-found page (GitHub Pages serves it automatically). |
| `CNAME` | Your custom domain for GitHub Pages. |
| `robots.txt` / `sitemap.xml` | SEO — let search engines index you. |
| `.github/workflows/deploy.yml` | Auto-deploys to GitHub Pages on push. |
| `render.yaml` | Alternative: deploy as a Render Static Site. |

---

## 🚀 3. Deploy — Option A: GitHub Pages (recommended, free)

1. Push this folder to a repo named `portfolio` (or `<username>.github.io`).
2. **Settings → Pages → Source: GitHub Actions.**
3. Push to `main` → the `deploy.yml` workflow publishes the site.
4. Live at `https://<username>.github.io/portfolio/`.

### Custom domain
1. Buy a cheap domain (Namecheap/Porkbun/Cloudflare, ~$10/yr).
2. Keep the `CNAME` file (set it to your domain, e.g. `yourname.dev`).
3. At your registrar, add DNS records pointing to GitHub Pages:
   - `A` records → `185.199.108.153`, `.109.153`, `.110.153`, `.111.153`
   - or a `CNAME` for `www` → `<username>.github.io`
4. **Settings → Pages → Custom domain** → enter your domain → **Enforce HTTPS**.

## 🚀 3. Deploy — Option B: Render Static Site
**New → Static Site** → connect the repo → Publish directory `.` → Create. Or push
`render.yaml` and use **New → Blueprint**. Add your custom domain under the
service's **Settings → Custom Domains** (Render issues the cert automatically).

---

## ⚡ 4. Performance & SEO checklist

- [x] Single CSS file, system fonts, inline SVG favicon → **no render-blocking requests**
- [x] Static gzip/Brotli compression (GitHub Pages & Render do this automatically; WhiteNoise on the Django sites)
- [x] `<meta name="description">`, Open Graph & Twitter cards, `canonical`
- [x] `robots.txt` + `sitemap.xml`
- [x] Polished `404.html`
- [x] Responsive down to 360px, `theme-color` for mobile browser chrome

---

## 🧪 5. Test locally

It's plain static files — just open `index.html`, or serve it:
```bash
python -m http.server 8000
# visit http://127.0.0.1:8000/
```
Check: every project card opens its live URL, the layout is responsive, and
visiting a bad path (on the deployed site) shows the styled 404.

---

## 🎯 6. Why this is the project that matters

This becomes the **single link at the top of your resume**. From here a recruiter
can click straight into a running blog, a student CRUD with uploads, a documented
REST API, and an e-commerce store — proof you can not just build, but **ship**.

# 🟢 Project 1 — Personal Portfolio Repository (solo basics)

**Goal:** put your **Module 3 portfolio site** under version control, push it to
GitHub, and deploy it **live and free** with GitHub Pages. Along the way you
learn the **solo loop** — the everyday rhythm of `edit → add → commit → push`
that every later project builds on.

> **In one sentence:** you'll end with a portfolio website that is *itself
> hosted in a portfolio-quality repository* — proof you can use Git.

This is a **demo walkthrough**, not an app. Read it top to bottom, then do every
step on a **real GitHub repo** of your own. Files in this folder
([.gitignore.sample](.gitignore.sample), [README.template.md](README.template.md),
[commit-log.txt](commit-log.txt), [branch-diagram.txt](branch-diagram.txt)) are
**reference copies** to compare your work against.

---

## 📑 Table of Contents
1. [What you'll build](#-1-what-youll-build)
2. [The solo loop (the one picture to remember)](#-2-the-solo-loop-the-one-picture-to-remember)
3. [Step 1 — Repository setup (init → commit → push)](#-step-1--repository-setup-init--commit--push)
4. [Step 2 — Deploy free with GitHub Pages](#-step-2--deploy-free-with-github-pages-bonus)
5. [Step 3 — Practice ONE feature branch](#-step-3--practice-one-feature-branch)
6. [Step 4 — Open a PR to your own repo & self-review](#-step-4--open-a-pr-to-your-own-repo--self-review)
7. [Commit standards](#-commit-standards)
8. [Deliverables checklist](#-deliverables-checklist)
9. [Troubleshooting](#-troubleshooting)

---

## 🎯 1. What you'll build

You already have a portfolio site folder from Module 3 (HTML/CSS, maybe a little
JS). Right now it lives only on your laptop. By the end of this project it will
be:

- **Versioned** — every change saved with a message, undoable forever.
- **On GitHub** — backed up in the cloud at a public URL.
- **Live** — anyone in the world can visit it via GitHub Pages.
- **Documented** — a clean README so visitors (and recruiters) know what it is.

---

## 🔁 2. The solo loop (the one picture to remember)

Even alone, every change follows the same four moves:

```
   ┌─────────────────────────────────────────────────────────┐
   │                                                         │
   │   1. EDIT          2. STAGE         3. COMMIT     4. PUSH│
   │   (change files)   git add .        git commit    git push
   │        │              │                 │            │   │
   │        ▼              ▼                 ▼            ▼   │
   │   index.html ───▶ [staged] ───▶ [saved snapshot] ─▶ GitHub
   │                                                         │
   └─────────────────────────────────────────────────────────┘
                          ▲                              │
                          └──── git pull (bring down) ◀──┘
```

Memorise this. Projects 2–5 are just this loop with more people and more rules.

---

## ▶️ Step 1 — Repository setup (init → commit → push)

Open a terminal **inside your portfolio folder** and run these in order.

```bash
# 1. Turn this folder into a git repository
git init

# 2. Create a .gitignore so junk never gets committed
#    (copy from .gitignore.sample in this folder)
#    On macOS this hides Finder's .DS_Store; node_modules/ if you used npm.

# 3. Stage everything that isn't ignored
git add .

# 4. Take the first snapshot
git commit -m "feat: initial portfolio"

# 5. Create an EMPTY repo on github.com (no README, no .gitignore — you have those)
#    then connect your local repo to it:
git remote add origin https://github.com/<your-username>/portfolio.git

# 6. Rename your branch to main (if it isn't already) and push
git branch -M main
git push -u origin main
```

**What just happened, visualized:**

```
  BEFORE                          AFTER  `git push -u origin main`
  ──────                          ─────────────────────────────────
  laptop only                     laptop  ⇄  GitHub (origin)
  ┌───────────┐                   ┌───────────┐     ┌───────────┐
  │ main      │                   │ main      │ ──▶ │ main      │
  │  ● initial│                   │  ● initial│     │  ● initial│
  └───────────┘                   └───────────┘     └───────────┘
                                  (the -u flag links them so next
                                   time you can just type `git push`)
```

### Your `.gitignore` (copy this — see [.gitignore.sample](.gitignore.sample))

```gitignore
# OS junk
.DS_Store
Thumbs.db

# Node (only if you used npm/build tools)
node_modules/
dist/

# Editor
.vscode/
.idea/
```

> 💡 **Why `.gitignore` first?** Once a file is committed it's in history
> forever. Ignoring it *before* the first commit keeps your history clean. You'll
> feel the full weight of this in Project 2 (databases & secrets).

---

## 🌐 Step 2 — Deploy free with GitHub Pages (bonus)

GitHub will host your static site for free:

1. On GitHub, open your repo → **Settings** → **Pages**.
2. Under **Build and deployment → Source**, pick **Deploy from a branch**.
3. Choose branch **`main`**, folder **`/ (root)`**, click **Save**.
4. Wait ~1 minute, then refresh. GitHub shows your live URL:

```
   https://<your-username>.github.io/portfolio/
```

That URL is now **live to the entire internet**. Every time you `git push`,
the live site updates automatically. 🎉

```
   git push  ──▶  GitHub main branch  ──▶  GitHub Pages rebuilds  ──▶  live URL updates
```

---

## 🌿 Step 3 — Practice ONE feature branch

Solo, you *could* work straight on `main` for tiny edits. But you should
**practice branching once** here, because it's the foundation of every team
project. Let's add a "Projects" section on its own branch.

```bash
# Create AND switch to a new branch in one command
git switch -c add-projects-section

# ... edit index.html to add the new section ...

git add index.html
git commit -m "feat: add projects showcase section"

# Push the branch up to GitHub
git push -u origin add-projects-section
```

**Branch picture** (also in [branch-diagram.txt](branch-diagram.txt)):

```
  main                ● initial ─────────────────────────● (merge)
                                 \                       /
  add-projects-section            ●─── feat: add projects section
```

The two branches diverge, then rejoin when you merge. `main` stays safe and
deployable the whole time.

---

## 🔍 Step 4 — Open a PR to your own repo & self-review

A **Pull Request (PR)** says "please pull these commits from my branch into
`main`." Even solo, opening one builds a great habit: **you read your own diff
before it lands.**

1. After pushing, GitHub shows a yellow banner: **"Compare & pull request"** — click it.
2. Base = `main`, Compare = `add-projects-section`.
3. Write a short description: *"Adds a Projects section showcasing 3 builds."*
4. Click **Files changed** and **read every line** — this is the self-review. Ask:
   does each change belong? Any leftover `console.log`? Any typo?
5. Click **Create pull request**, then **Merge pull request** → **Confirm merge**.
6. Click **Delete branch** (it's merged; the commits live on in `main`).
7. Back on your laptop, sync up:

```bash
git switch main
git pull            # brings the merged commit down from GitHub
git branch -d add-projects-section   # delete the local copy too
```

**Full lifecycle, visualized:**

```
  edit ─▶ commit ─▶ push branch ─▶ open PR ─▶ self-review diff ─▶ merge ─▶ pull ─▶ delete branch
   1        2          3            4           5                  6        7         8
```

---

## ✍️ Commit standards

Typed + imperative. For a portfolio you'll mostly use:

```
feat:  add hero section with intro and photo
feat:  add projects showcase section
style: improve mobile nav spacing
docs:  write README with live demo link
fix:   correct broken link to resume PDF
```

See [commit-log.txt](commit-log.txt) for a full example of what a healthy
portfolio history looks like.

---

## ✅ Deliverables checklist

- [ ] Repo on GitHub with a clean first commit (`feat: initial portfolio`).
- [ ] A `.gitignore` that excludes OS junk (and `node_modules/` if relevant).
- [ ] A clean **README** (use [README.template.md](README.template.md)) with a
      one-line description and the **live demo link**.
- [ ] **Live GitHub Pages URL** that loads your site.
- [ ] At least one **feature branch** that was **PR'd, self-reviewed, merged,**
      and **deleted**.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `fatal: not a git repository` | You're not inside the folder, or forgot `git init`. |
| `remote origin already exists` | `git remote set-url origin <url>` to fix the URL instead. |
| Push rejected, "updates were rejected" | The GitHub repo had a README you didn't have. Run `git pull --rebase origin main`, then push. |
| GitHub Pages shows 404 | Check Settings → Pages branch is `main` / root; wait 1–2 min; ensure your homepage is named `index.html`. |
| Committed `.DS_Store` by accident | `git rm --cached .DS_Store`, add it to `.gitignore`, commit again. |
| Want to undo the last commit (not pushed) | `git reset --soft HEAD~1` keeps your changes, drops the commit. |

---

➡️ **Next:** [Project 2 — Django Blog Repository](../project_2_django_blog_repo/),
where the `.gitignore` becomes life-or-death (databases & secrets) and you run a
real feature-branch loop.

# 🟡 Project 2 — Django Blog Repository (solo, real `.gitignore` + branches)

**Goal:** version-control your **Module 4 blog** (`project_3_blog_management_system`)
the *professional* way — with a **production-grade `.gitignore`** that keeps
databases and secrets out of history, and a **real feature-branch loop** (GitHub
Flow). This is where you learn the rule that saves careers: **never commit
secrets or the database.**

> **In one sentence:** Project 1 taught you the loop; Project 2 teaches you what
> *not* to commit, and how to run one branch per feature.

This is a **demo walkthrough**. Read it, then do it on a real GitHub repo using
your actual Module 4 blog code. Reference copies in this folder:
[.gitignore.sample](.gitignore.sample),
[requirements.sample.txt](requirements.sample.txt),
[PULL_REQUEST_TEMPLATE.md](PULL_REQUEST_TEMPLATE.md),
[commit-log.txt](commit-log.txt), [branch-diagram.txt](branch-diagram.txt).

---

## 📑 Table of Contents
1. [Why `.gitignore` first matters SO much here](#-1-why-gitignore-first-matters-so-much-here)
2. [Step 1 — Setup: .gitignore FIRST, then commit](#-step-1--setup-gitignore-first-then-commit)
3. [GitHub Flow — the branch strategy](#-github-flow--the-branch-strategy)
4. [Step 2 — Build a feature on its own branch](#-step-2--build-a-feature-on-its-own-branch)
5. [Step 3 — PR, self-review, squash-merge, clean up](#-step-3--pr-self-review-squash-merge-clean-up)
6. [Commit standards](#-commit-standards)
7. [Deliverables checklist](#-deliverables-checklist)
8. [Troubleshooting](#-troubleshooting)

---

## 🔒 1. Why `.gitignore` first matters SO much here

A Django project is **not** just your code. After you run it, the folder also
contains things that must **never** go to GitHub:

```
   blog_project/
   ├── blog/            ← YOUR CODE  ✅ commit this
   ├── config/          ← YOUR CODE  ✅ commit this
   ├── manage.py        ← YOUR CODE  ✅ commit this
   ├── requirements.txt ← the LIST of libs ✅ commit this
   │
   ├── venv/            ← 100s of MB of installed libraries  ❌ NEVER commit
   ├── db.sqlite3       ← your database, with real data       ❌ NEVER commit
   ├── __pycache__/     ← compiled Python bytecode            ❌ NEVER commit
   ├── .env             ← SECRET_KEY, passwords, API keys      ❌ NEVER commit
   └── media/           ← user-uploaded files                 ❌ NEVER commit
```

**Why it's serious:**
- A committed `.env` leaks your `SECRET_KEY` — anyone can forge sessions.
- A committed `db.sqlite3` leaks real user data and bloats the repo.
- A committed `venv/` is huge, OS-specific, and useless to others (they rebuild it from `requirements.txt`).

And the kicker: **once something is committed, it stays in history even if you
delete it later.** Removing a leaked secret means rewriting history — painful.
So you ignore these **before the first `git add`.**

```
   requirements.txt  ──(others run)──▶  pip install -r requirements.txt  ──▶  rebuilds venv/
        ✅ tiny, portable                                                       ❌ never in git
```

---

## ▶️ Step 1 — Setup: `.gitignore` FIRST, then commit

Run inside your Module 4 blog folder, **in this order**:

```bash
# 1. Create .gitignore BEFORE anything else (copy from .gitignore.sample here)
#    It must already contain: venv/  db.sqlite3  __pycache__/  .env  /media/

# 2. NOW initialise git — nothing ignored will ever be tracked
git init

# 3. Make sure your secrets live in .env (not in settings.py!) and that
#    requirements.txt exists:
pip freeze > requirements.txt

# 4. Stage and verify — CHECK that venv/ and db.sqlite3 are NOT listed:
git add .
git status        # ⚠️ if you see venv/ or db.sqlite3 here, STOP and fix .gitignore

# 5. First commit
git commit -m "feat: initial Django blog"

# 6. Create an empty GitHub repo, then connect & push
git remote add origin https://github.com/<you>/django-blog.git
git branch -M main
git push -u origin main
```

> 🛑 **The one check that matters:** after `git add .`, run `git status` and
> confirm `venv/`, `db.sqlite3`, and `.env` are **NOT** in the list. If they are,
> they're not being ignored — fix `.gitignore` and `git rm --cached <file>` them.

---

## 🌊 GitHub Flow — the branch strategy

GitHub Flow is the simplest professional model and the one you'll use for the
rest of the module:

```
   RULE 1:  main is ALWAYS runnable (never commit broken code to main).
   RULE 2:  every change happens on a short-lived branch off main.
   RULE 3:  merge back via a Pull Request, then delete the branch.

   main  ●──────────●──────────────────●──────────────●  (always green)
          \        / \                / \            /
           feature/  feature/        fix/          feature/
           comments  categories      slug-duplicate tags
```

**Branch naming** — describe the work with a type prefix:

```
   feature/comments          fix/slug-duplicate
   feature/categories        fix/broken-pagination
```

---

## 🌿 Step 2 — Build a feature on its own branch

Let's add **comments** to the blog. Each *logical unit* gets its own commit.

```bash
# Always start from an up-to-date main
git switch main
git pull

# Create the feature branch
git switch -c feature/comments

# --- commit 1: the data layer ---
#   edit blog/models.py (add Comment model) + blog/forms.py (add CommentForm)
git add blog/models.py blog/forms.py
git commit -m "feat: add Comment model and form"

# --- commit 2: wire it into the page ---
#   edit blog/views.py + templates to render comments on post detail
git add blog/views.py blog/templates/
git commit -m "feat: render comments on post detail page"

# --- commit 3: prove it works ---
#   edit blog/tests.py
git add blog/tests.py
git commit -m "test: add comment submission test"

# Push the branch up
git push -u origin feature/comments
```

Notice the rhythm: **one logical change = one commit.** Three small, clear
commits beat one giant "added comments" blob. Reviewers (and future you) can
read the story.

---

## 🔍 Step 3 — PR, self-review, squash-merge, clean up

1. GitHub shows **"Compare & pull request"** — click it.
2. Fill in the PR using [PULL_REQUEST_TEMPLATE.md](PULL_REQUEST_TEMPLATE.md).
   A good description:

   > **Adds threaded comments to blog posts.**
   > Readers can submit a comment on the post-detail page; it's saved and
   > rendered immediately. Includes a model, form, view wiring, and a test.
   > Closes #3.

3. Open **Files changed** and self-review every line. Confirm: no `print()`
   debug left in, no `db.sqlite3` in the diff, migrations included.
4. Merge using **Squash and merge** — this combines your 3 work commits into
   **one tidy commit on `main`**, keeping history clean.
5. **Delete branch** on GitHub.
6. Sync your laptop:

```bash
git switch main
git pull
git branch -d feature/comments
```

**Squash-merge, visualized:**

```
  feature/comments:   ● model ── ● render ── ● test       (3 messy work commits)
                                                  \
                                                   ▼  "Squash and merge"
  main:  ●───────────────────────────────────────● feat: add post comments (#4)
                                                    (1 clean commit on main)
```

---

## ✍️ Commit standards

One logical unit per commit, typed + imperative:

```
feat: add Comment model and form
feat: render comments on post detail page
test: add comment submission test
fix:  prevent duplicate slugs on post save
docs: document comment feature in README
chore: add production .gitignore
```

See [commit-log.txt](commit-log.txt) for the full target history.

---

## ✅ Deliverables checklist

- [ ] `.gitignore` created **before** the first commit, excluding `venv/`,
      `db.sqlite3`, `__pycache__/`, `.env`, `/media/`.
- [ ] `git status` proves none of the above are tracked.
- [ ] `requirements.txt` committed (the **list**, not `venv/`).
- [ ] At least one **`feature/...` branch** built with **multiple logical commits**.
- [ ] A PR with a real description that links an issue (`Closes #3`), self-reviewed.
- [ ] **Squash-merged**, branch **deleted**, `main` pulled.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `venv/` shows up in `git status` | It's not ignored. Add `venv/` to `.gitignore`, then `git rm -r --cached venv` and commit. |
| Already committed `db.sqlite3` | `git rm --cached db.sqlite3`, add it to `.gitignore`, commit `chore: stop tracking database`. |
| Already pushed a `.env` with secrets | Rotate the secret immediately (it's compromised), then remove it from history (`git filter-repo` or BFG) and force-push. Prevention > cure. |
| `git switch -c` fails: "already exists" | The branch exists — use `git switch <branch>` to jump to it. |
| Forgot to branch, committed to `main` | `git switch -c feature/x` then `git switch main && git reset --hard origin/main` to move the work onto a branch (careful — only if not pushed). |
| PR can't merge: "conflicts" | `main` moved on. `git switch feature/x; git merge main`, resolve, push. (Full conflict drill is in Project 3.) |

---

➡️ **Next:** [Project 3 — Team Student Management System](../project_3_team_student_mgmt/),
where you stop working alone: protected `main`, code reviews, and a deliberate
merge conflict you resolve with a teammate.

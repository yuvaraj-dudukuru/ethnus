# 🌳 Module 7 — Git & GitHub: From Solo Commits to Open Source

Welcome to Module 7. **There are no new apps here.** Instead, these five
projects teach you the **Git & GitHub workflows** for the apps you *already
built* in Modules 4–6. You take working code and learn to **version it,
collaborate on it, review it, automate it, and contribute to other people's
projects** — the daily skills of every professional developer.

> **In one sentence:** Modules 4–6 taught you to *build* software. Module 7
> teaches you to *work on software with other people* — the part that actually
> gets you hired.

Each project is a **guided demo**: a heavily-explained, visual walkthrough you
run on a **real repository**. Do them **in order** — each one adds one new
muscle on top of the last.

---

## 🎚️ The progression (do them in this order)

```
 SOLO  ───────────────────────────────────────────────▶  TEAM  ─────▶  OPEN SOURCE

 🟢 P1            🟡 P2            🟠 P3 ⭐          🔵 P4            🔴 P5 ⭐
 Portfolio        Django Blog      Team Student      REST API         Open Source
 (the basics)     (real .gitignore  Management        (CI/CD intro)    Contribution
                   + branches)      (collaboration)                    (the capstone)
   │                │                │                 │                │
   │ git init       │ feature        │ protected main  │ GitHub         │ fork →
   │ commit         │ branches       │ + PR reviews    │ Actions        │ upstream →
   │ push           │ secrets out    │ + merge         │ green-check    │ PR to a repo
   │ GitHub Pages   │ of history     │ conflicts       │ gates          │ you don't own
```

| # | Project | References | New muscle you build |
|---|---------|-----------|----------------------|
| 🟢 **1** | [Personal Portfolio Repository](./project_1_portfolio_repo/) | Module 3 portfolio | `init → commit → push`, GitHub Pages, the solo loop |
| 🟡 **2** | [Django Blog Repository](./project_2_django_blog_repo/) | Module 4 blog | Production `.gitignore`, secrets out of history, feature branches |
| 🟠 **3** | [Team Student Management System](./project_3_team_student_mgmt/) ⭐ | Module 4/6 dashboard | Protected `main`, PRs, code review, **merge conflicts** |
| 🔵 **4** | [REST API Repository](./project_4_rest_api_repo/) | Module 5 DRF API | **CI/CD** with GitHub Actions, automated quality gates |
| 🔴 **5** | [Open Source Contribution](./project_5_open_source_sim/) ⭐ | any public repo | The **fork → upstream → PR** flow, contributing to others' code |

---

## 🧠 The mental model (read this once)

Everything in this module is built out of just a few moving parts. Picture them
like this:

```
   YOUR LAPTOP                              GITHUB (the cloud)
   ───────────                              ─────────────────
                                          ┌──────────────────────┐
   working files ──┐                      │   origin  (your repo) │
        │ git add  │                      │   ┌────────────────┐  │
        ▼          │      git push        │   │   main branch  │  │
   staging area ───┼──────────────────────┼──▶│  feature/x ... │  │
        │ git commit                      │   └────────────────┘  │
        ▼          │      git pull        │            ▲          │
   local repo  ◀───┴──────────────────────┼────────────┘          │
   (history)                              │   Pull Requests, CI,   │
                                          │   reviews, Pages       │
                                          └──────────────────────┘
```

- **working files** — the code you edit.
- **staging area** — the box of changes you've marked (`git add`) to go in the next commit.
- **local repo** — the full history of commits on your machine.
- **origin** — your copy on GitHub. `push` sends commits up; `pull` brings them down.
- **upstream** (Project 5 only) — *someone else's* repo that you forked from.

---

## ✍️ Commit message standard (used in every project)

We use **Conventional Commits**: a `type:` prefix + an **imperative** summary
("add", not "added"). This single habit makes your history readable and is
expected at almost every company.

| Type | Use it for | Example |
|------|-----------|---------|
| `feat` | a new feature | `feat: add comment form to post detail` |
| `fix` | a bug fix | `fix: prevent duplicate slugs on save` |
| `docs` | documentation only | `docs: write setup section in README` |
| `style` | formatting, CSS, no logic change | `style: improve mobile nav spacing` |
| `refactor` | restructure, same behaviour | `refactor: extract pagination helper` |
| `test` | adding/fixing tests | `test: cover student list endpoint` |
| `ci` | CI/CD config | `ci: add GitHub Actions test workflow` |
| `chore` | tooling, deps, housekeeping | `chore: add .gitignore` |

**Rule of thumb:** one commit = one logical change. Link issues in the body
with `Closes #12`.

---

## 🗂️ What's inside each project folder

Because these are workflow demos, each folder contains the **real artifacts**
that workflow produces, so you can read and reuse them:

- `README.md` — the visual, step-by-step walkthrough.
- `.gitignore` examples, PR/issue templates, `LICENSE`, `CONTRIBUTING.md`,
  GitHub Actions YAML — whichever the project teaches.
- `commit-log.txt` / `branch-diagram.txt` — a **simulated** picture of what your
  history *should* look like when you're done, so you have a target to compare against.

> Files named with `.sample` or living under `examples/` are **reference copies**
> for you to read. When you do the project for real, you create the *actual*
> files in *your* repo.

---

## ✅ How to use this module

1. Open **Project 1** and read its README top to bottom.
2. Do it on a **real repo** (your own GitHub account — it's free).
3. Compare your result to the `commit-log.txt` / diagrams in the folder.
4. Move to the next project. Don't skip — each assumes the last.

By the end you'll have, **publicly on your GitHub profile**: a deployed
portfolio, a clean Django repo with no leaked secrets, a team project with
reviewed PRs and a resolved merge conflict, a repo with a green CI badge, and a
merged open-source contribution. That last line is the most credible thing a
junior developer can put on a resume.

Happy collaborating! 🌳

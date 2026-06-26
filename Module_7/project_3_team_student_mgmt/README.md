# 🟠 Project 3 — Team-Based Student Management System ⭐ (collaboration core)

**Goal:** simulate a **real software team** working on the **Module 4/6 Student
Management dashboard** — one shared repo, protected `main`, issues, peer code
reviews, and the single most important learning moment in this whole module:
**deliberately creating a merge conflict and resolving it together.**

> **In one sentence:** Projects 1–2 were you, alone. Project 3 is *a team* —
> parallel work, reviews, protected `main`, and conflict resolution. This is the
> heart of Module 7.

This is a **demo walkthrough** for a group (ideally 2–4 students; you can also
play both roles solo with two GitHub accounts or two clones). Reference copies:
[CODEOWNERS](CODEOWNERS),
[PULL_REQUEST_TEMPLATE.md](PULL_REQUEST_TEMPLATE.md),
[ISSUE_TEMPLATE.md](ISSUE_TEMPLATE.md),
[merge_conflict_demo/](merge_conflict_demo/) ← **the key exercise**,
[commit-log.txt](commit-log.txt), [branch-diagram.txt](branch-diagram.txt).

---

## 📑 Table of Contents
1. [The team workflow at a glance](#-1-the-team-workflow-at-a-glance)
2. [Step 1 — Shared repo + protected main](#-step-1--shared-repo--protected-main)
3. [Step 2 — Plan work on the Issues board](#-step-2--plan-work-on-the-issues-board-kanban)
4. [Step 3 — Each dev: branch → build → PR → review](#-step-3--each-dev-branch--build--pr--review)
5. [⭐ Step 4 — The merge conflict drill (DO THIS TOGETHER)](#-step-4--the-merge-conflict-drill-do-this-together)
6. [Branch & commit standards](#-branch--commit-standards)
7. [Deliverables checklist](#-deliverables-checklist)
8. [Troubleshooting](#-troubleshooting)

---

## 🗺️ 1. The team workflow at a glance

```
   ISSUES (plan)        BRANCHES (build)         PR + REVIEW (check)       MERGE
   ────────────         ────────────────         ───────────────────      ─────
   #12 add filter  ──▶  alice/feature/filter ──▶  PR ──▶ Bob reviews  ──▶  ✔ approve ──▶ squash-merge
   #13 fix nav     ──▶  bob/fix/nav         ──▶  PR ──▶ Alice reviews ──▶  ✔ approve ──▶ squash-merge
                                                       │
                                                       ▼
                              main is PROTECTED: no direct pushes,
                              every change needs 1 approval + green CI

   ┌───────────────────────────────────────────────────────────────────┐
   │  main  ●────────────●──────────────●─────────────────●             │
   │         \          / \            /                                 │
   │          alice/...    bob/...   (parallel work by different people) │
   └───────────────────────────────────────────────────────────────────┘
```

---

## ▶️ Step 1 — Shared repo + protected main

**One** person creates the repo (from the Module 4/6 student dashboard code) and
adds the others:

1. Create the repo, push the dashboard code (use the Project 2 `.gitignore`!).
2. **Settings → Collaborators → Add people** → add each teammate.
   *(Alternative: each teammate **forks** instead of being a collaborator — same
   PR flow, just from their fork.)*
3. **Protect `main`** so nobody can push to it directly:
   **Settings → Branches → Add branch ruleset** (or "Add rule") for `main`:
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals: 1**
   - ✅ **Require status checks to pass** (if you add CI in Project 4)
   - ✅ **Do not allow bypassing the above settings**

```
   BEFORE protection            AFTER protection
   ─────────────────            ────────────────
   anyone → git push main  ✅    git push main  ✗  REJECTED
   (chaos, broken main)         must open PR → get 1 approval → merge ✅
```

This single setting is what makes it a *team* repo instead of a free-for-all.

---

## 📋 Step 2 — Plan work on the Issues board (Kanban)

Before anyone codes, the team plans:

1. **Issues** tab → create an issue per task (use [ISSUE_TEMPLATE.md](ISSUE_TEMPLATE.md)):
   - `#11 Add department filter to dashboard`
   - `#12 Add "Export CSV" button`
   - `#13 Redesign the dashboard navigation bar`
2. Add **labels** (`feature`, `bug`, `good first issue`) and a **milestone** (`v1.0`).
3. **Projects** tab → create a **board** with columns `To Do / In Progress / Done`.
4. **Assign** each issue to a teammate and drag it to `In Progress` when they start.

```
   ┌─ To Do ──────┐  ┌─ In Progress ─┐  ┌─ Done ───────┐
   │ #12 Export   │  │ #11 Filter    │  │ (merged PRs  │
   │     CSV      │  │   @alice      │  │  land here)  │
   │ #13 Nav      │  │ #13 Nav       │  │              │
   │   redesign   │  │   @bob        │  │              │
   └──────────────┘  └───────────────┘  └──────────────┘
```

---

## 🌿 Step 3 — Each dev: branch → build → PR → review

Every teammate, for their assigned issue:

```bash
# ALWAYS start from the latest main (others may have merged since)
git switch main
git pull

# Branch — naming convention: <author>/<type>/<name>
git switch -c alice/feature/department-filter

# ...build the feature, commit in logical units...
git add students/ static/
git commit -m "feat: add department dropdown filter to dashboard

Closes #11"

git push -u origin alice/feature/department-filter
```

Then open a PR and get a **peer review** (this is the new muscle):

- The PR author requests a reviewer (a teammate).
- The reviewer opens **Files changed**, clicks a line, and leaves comments:
  **Request changes** ("this breaks search when filter is empty") or **Approve**.
- Author pushes fixes; reviewer re-checks; on approval → **Squash and merge**.
- Everyone else runs `git switch main && git pull` to get the new code.

```
   author        reviewer
   ──────        ────────
   open PR  ──▶  read diff ──▶ 💬 request changes ──▶ author pushes fix
                                      │                        │
                                      └──── ✔ approve ◀─────────┘
                                              │
                                              ▼  squash-merge → others pull
```

---

## ⭐ Step 4 — The merge conflict drill (DO THIS TOGETHER)

**This is the most important exercise in Module 7.** You will *deliberately*
make two people edit the **same lines** of the dashboard nav, so Git can't
auto-merge — then resolve it as a team.

The full hands-on files are in **[merge_conflict_demo/](merge_conflict_demo/)**:
- [base_nav.html](merge_conflict_demo/base_nav.html) — the starting nav both devs branch from.
- [alice_version.html](merge_conflict_demo/alice_version.html) — Alice's edit.
- [bob_version.html](merge_conflict_demo/bob_version.html) — Bob's *conflicting* edit.
- [conflicted_nav.html](merge_conflict_demo/conflicted_nav.html) — what Git produces (the `<<<<<<<` markers).
- [resolved_nav.html](merge_conflict_demo/resolved_nav.html) — the agreed final result.
- [WALKTHROUGH.md](merge_conflict_demo/WALKTHROUGH.md) — the exact commands, step by step.

### Why a conflict happens (the picture)

```
                          ● base: <nav> ... </nav>   (both start here)
                         / \
   alice/nav  edits LINE 3  \  bob/nav ALSO edits LINE 3
            │                \           │
            ● "Students | Reports"        ● "Dashboard | Settings"
            │                            │
   Alice's PR merges first ✅            Bob's PR now CONFLICTS:
                                         Git: "you both changed line 3,
                                          I can't choose — you decide."
```

### What Git shows you (conflict markers)

```html
<<<<<<< HEAD                         (what's already on main — Alice's)
  <a href="/">Students</a> | <a href="/reports">Reports</a>
=======                             (the divider)
  <a href="/">Dashboard</a> | <a href="/settings">Settings</a>
>>>>>>> bob/fix/nav                 (what Bob's branch wants)
```

### Resolving it (the human part)

1. Bob runs `git switch bob/fix/nav` then `git merge main` → Git reports the conflict.
2. Bob + Alice **talk**: "let's keep all four links."
3. Edit the file to the agreed version (delete the `<<<<`, `====`, `>>>>` markers):
   ```html
   <a href="/">Students</a> | <a href="/reports">Reports</a> |
   <a href="/settings">Settings</a>
   ```
4. `git add base_nav.html` → `git commit` (Git pre-fills a merge message) → `git push`.
5. The PR goes green; reviewer approves; squash-merge. **Conflict resolved.** 🎉

> 📖 The exact command transcript is in
> [merge_conflict_demo/WALKTHROUGH.md](merge_conflict_demo/WALKTHROUGH.md). Run it
> for real — *experiencing* a conflict once removes the fear forever.

---

## 🌿 Branch & commit standards

```
   Branch naming:   <author>/<type>/<name>
                    alice/feature/department-filter
                    bob/fix/nav-overlap
                    feature/export-csv          (author prefix optional but nice)

   Commits:         Conventional Commits, enforced in review.
                    feat: add department dropdown filter to dashboard
                    Link the issue in the body or footer:  Closes #11
```

**Always `git pull` on `main` before branching** — your teammates may have
merged work you need.

---

## ✅ Deliverables checklist

- [ ] One shared repo; all teammates are collaborators (or forking).
- [ ] `main` is **protected**: PR required, **1 approval** required, no direct push.
- [ ] An **Issues board** with assigned, labelled issues + a milestone.
- [ ] Each dev landed at least one PR that another teammate **reviewed & approved**.
- [ ] At least one PR had a **"Request changes"** round before approval.
- [ ] A **merge conflict was deliberately created and resolved together**.
- [ ] History is clean (squash-merge), branches deleted after merge.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| Can't push to `main` | That's correct — it's protected. Open a PR instead. |
| "Review required" blocks merge | A teammate must **Approve** the PR first. |
| Reviewer can't approve their own PR | GitHub forbids self-approval on protected branches — ask another teammate. |
| Conflict feels scary | Read `merge_conflict_demo/WALKTHROUGH.md`; conflicts are normal and fixable. |
| `git merge main` says "Already up to date" | Run `git switch main && git pull` first, then merge into your branch. |
| Pulled and lost track of branches | `git branch -a` lists all; `git branch -d <name>` deletes merged ones. |
| Two people assigned the same issue | Talk first; one takes it, the other picks another — that's the point of the board. |

---

➡️ **Next:** [Project 4 — REST API Repository](../project_4_rest_api_repo/),
where you add **automated quality gates**: GitHub Actions runs your tests on
every PR, and red tests **block the merge**.

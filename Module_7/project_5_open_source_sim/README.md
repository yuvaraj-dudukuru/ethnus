# 🔴 Project 5 — Open Source Contribution Simulation ⭐ (capstone)

**Goal:** make a **real (or realistic) contribution to a project you don't own.**
You'll fork someone else's repo, branch a focused change, push it to *your* fork,
and open a Pull Request **to the original project** — then respond to maintainer
feedback. This is the **fork → upstream → PR** flow, and a merged PR on a public
repo is the single most credible line on a junior developer's resume.

> **In one sentence:** Projects 1–4 were *your* repos. Project 5 is working
> inside *someone else's* — their rules, their reviewers, your contribution.

This is a **demo walkthrough**. If you can, do it for real on a tiny
`good first issue` (a typo fix counts!). If you want to rehearse safely first,
use the included practice repo: [practice_upstream_repo/](practice_upstream_repo/).
Reference copies: [CONTRIBUTING.md](CONTRIBUTING.md),
[sample_pr_description.md](sample_pr_description.md),
[fork-flow-diagram.txt](fork-flow-diagram.txt),
[commit-log.txt](commit-log.txt).

---

## 📑 Table of Contents
1. [The three repos you'll juggle (the mental model)](#-1-the-three-repos-youll-juggle-the-mental-model)
2. [Step 1 — Find a beginner-friendly issue](#-step-1--find-a-beginner-friendly-issue)
3. [Step 2 — Fork & clone & wire up upstream](#-step-2--fork--clone--wire-up-upstream)
4. [Step 3 — Branch a focused change](#-step-3--branch-a-focused-change)
5. [Step 4 — Follow CONTRIBUTING.md (sign-off etc.)](#-step-4--follow-contributingmd-sign-off-etc)
6. [Step 5 — Push to YOUR fork, open PR to THEIRS](#-step-5--push-to-your-fork-open-pr-to-theirs)
7. [Step 6 — Respond gracefully to review](#-step-6--respond-gracefully-to-review)
8. [Deliverables checklist](#-deliverables-checklist)
9. [Troubleshooting](#-troubleshooting)

---

## 🧠 1. The three repos you'll juggle (the mental model)

This is the part that confuses beginners. There are **three** copies, and `git`
talks to two remotes:

```
   ┌─────────────────────────┐        ┌─────────────────────────┐
   │  UPSTREAM                │ fork   │  ORIGIN (your fork)      │
   │  github.com/THEM/repo    │──────▶ │  github.com/YOU/repo     │
   │  (the original project)  │        │  (your copy on GitHub)   │
   └──────────┬──────────────-┘        └────────────┬────────────┘
              │ git pull upstream main               │ git push origin <branch>
              │ (stay in sync)                       │ (publish your work)
              ▼                                      ▼
            ┌──────────────────────────────────────────┐
            │  YOUR LAPTOP   (git clone of your fork)   │
            │  remotes:  origin   = YOUR fork           │
            │            upstream = THEIR original repo │
            └──────────────────────────────────────────┘

   The PR goes:   YOUR fork's branch  ───────▶  UPSTREAM's main
                  (you can write here)          (you CANNOT push here directly)
```

- **upstream** = the real project. You can *read* it, *pull* from it, *PR* to it
  — but you can't push to it.
- **origin** = your fork. You push your branch here, then ask upstream to pull it.

---

## 🔎 Step 1 — Find a beginner-friendly issue

On GitHub, search for friendly, low-risk work:

```
   label:"good first issue"  label:documentation  language:Python
   label:"good first issue"  is:open  django
```

Good starter contributions (lowest risk → highest):
1. **Fix a typo** in the README or docs.
2. **Clarify** a confusing sentence in the docs.
3. **Add a missing example** to documentation.
4. **Fix a small, well-described bug** labelled `good first issue`.

> 🎯 **Pick something tiny.** The goal of this project is to learn the *flow*,
> not to rewrite their codebase. A merged one-line typo fix teaches everything a
> 500-line feature would — with none of the friction.

**Before coding:** comment on the issue ("I'd like to work on this!") so you
don't duplicate someone else's effort, and **read their `CONTRIBUTING.md`.**

---

## 🍴 Step 2 — Fork & clone & wire up upstream

```bash
# 1. On GitHub, click "Fork" on THEIR repo. Now YOU/repo exists.

# 2. Clone YOUR fork (note: YOUR username) to your laptop
git clone https://github.com/<you>/<repo>.git
cd <repo>

# 3. Add the ORIGINAL repo as a second remote called "upstream"
git remote add upstream https://github.com/<them>/<repo>.git

# 4. Verify both remotes exist
git remote -v
#   origin    https://github.com/<you>/<repo>.git   (fetch & push) ← your fork
#   upstream  https://github.com/<them>/<repo>.git  (fetch & push) ← the original
```

```
   Fork (web)  →  Clone your fork  →  add upstream remote
      🍴              💻                   🔗
   THEM/repo  →   YOU/repo (local)  →  knows about BOTH repos
```

---

## 🌿 Step 3 — Branch a focused change

**Always sync with upstream first**, then branch:

```bash
# Pull the latest from the ORIGINAL project so you start current
git switch main
git pull upstream main

# One focused change = one branch with a descriptive name
git switch -c fix/typo-in-readme
```

Make **one focused change** (e.g. fix the typo in their `README.md`). Resist
scope creep — reviewers merge small, clear PRs fastest.

---

## ✒️ Step 4 — Follow CONTRIBUTING.md (sign-off etc.)

Every project has its own rules. **Read their `CONTRIBUTING.md` and obey it
exactly** — matching their conventions is half of being a good contributor. A
common requirement is a **sign-off** (the Developer Certificate of Origin):

```bash
git add README.md
git commit -s -m "docs: fix typo in installation section"
#        ▲
#        └─ the -s adds a "Signed-off-by: Your Name <email>" line,
#           which many projects (Linux, Docker, etc.) require.
```

See [CONTRIBUTING.md](CONTRIBUTING.md) in this folder for a typical example of
what a project asks for (commit style, sign-off, tests, branch naming).

---

## 🚀 Step 5 — Push to YOUR fork, open PR to THEIRS

```bash
# Push the branch to ORIGIN (your fork) — NOT upstream (you can't)
git push -u origin fix/typo-in-readme
```

Then on GitHub:

1. Go to **the original repo** (upstream). It shows a banner:
   **"Compare & pull request"** from your fork's branch — click it.
2. **Base repository** = `THEM/repo` `main`; **head repository** = `YOU/repo`
   `fix/typo-in-readme`. Double-check this — the base must be *their* repo.
3. Write a clear description (use [sample_pr_description.md](sample_pr_description.md)):
   what you changed, why, and the issue it closes.
4. Submit. ✅

```
   YOU/repo : fix/typo-in-readme  ───── Pull Request ─────▶  THEM/repo : main
        (head, your fork)                                      (base, original)
```

---

## 💬 Step 6 — Respond gracefully to review

The maintainer may **approve and merge**, or **request changes**. Both are wins
— you learn either way. The professional behaviour:

- **Thank them.** Reviews are volunteer work.
- If they request changes, make them on the **same branch** and push again —
  the PR updates automatically:
  ```bash
  # ...edit per their feedback...
  git add . && git commit -s -m "docs: address review — clarify wording"
  git push        # the open PR picks this up; no new PR needed
  ```
- Don't argue or take feedback personally. "Good point, fixed!" goes a long way.
- If they merge: 🎉 you have a **public, merged contribution** on your profile.

```
   open PR ─▶ maintainer reviews ─▶ "please tweak X" ─▶ you push fix ─▶ ✔ merged
                     │                                                    │
                     └──────────── or straight to ✔ merged ──────────────┘
```

---

## ✅ Deliverables checklist

- [ ] Forked a real (or the practice) repo and cloned **your fork**.
- [ ] Added an **`upstream`** remote pointing at the original.
- [ ] Synced with `git pull upstream main`, then branched a **focused** change.
- [ ] Followed their **`CONTRIBUTING.md`** (commit style, **sign-off** if required).
- [ ] Pushed to **origin** (your fork), opened a PR to **upstream**.
- [ ] Responded to review feedback (or learned from it).
- [ ] (Goal) A **merged PR** visible on your public GitHub profile.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `git push` rejected to upstream | You can't push to a repo you don't own — push to `origin` (your fork). |
| PR base is wrong (points at your fork) | On the PR page, set **base repository** to `THEM/repo` and base branch to `main`. |
| Your fork is behind the original | `git pull upstream main` then `git push origin main` to update your fork. |
| Maintainer asks you to "rebase" | `git pull --rebase upstream main`, resolve any conflicts, `git push --force-with-lease`. |
| Forgot the sign-off they require | Amend it: `git commit --amend -s --no-edit`, then `git push --force-with-lease`. |
| No reply for weeks | Normal for volunteer projects — a polite "gentle ping?" comment after a week is fine. |
| Nervous about a real repo | Practice on [practice_upstream_repo/](practice_upstream_repo/) first, then go live. |

---

## 🎓 You finished Module 7

You can now: version code solo, keep secrets out of history, work on a team with
protected branches and reviews, resolve merge conflicts, gate merges with CI, and
contribute to projects you don't own. That's the full professional Git/GitHub
toolkit. **Go get that merged PR — it's the most credible line on your resume.**

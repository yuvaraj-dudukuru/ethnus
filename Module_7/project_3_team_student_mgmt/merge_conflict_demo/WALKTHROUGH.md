# ⭐ Merge Conflict Drill — exact command walkthrough

This is the **key learning moment** of Module 7. You will deliberately create a
merge conflict on the dashboard nav and resolve it. Run it for real — the fear
of conflicts disappears the moment you do one.

You need **two people** (Alice & Bob) — or play both roles yourself with two
terminal windows / two clones.

The files in this folder show every state: `base_nav.html` → `alice_version.html`
/ `bob_version.html` → `conflicted_nav.html` → `resolved_nav.html`.

---

## 0. Setup (once, on the shared repo)

Make sure `base_nav.html` (the starting nav) is committed on `main` and both
people have pulled it.

```bash
git switch main
git pull
```

---

## 1. Both devs branch from the SAME main

```bash
# ── Alice ──
git switch main && git pull
git switch -c alice/feature/reports-link

# ── Bob (at the same time) ──
git switch main && git pull
git switch -c bob/fix/nav-settings
```

Both are now editing from the identical starting point. This is what makes a
conflict possible.

---

## 2. Each edits the SAME line, commits, pushes

```bash
# ── Alice ── edits the nav line to add a Reports link
#   (make the file match alice_version.html)
git add base_nav.html
git commit -m "feat: add Reports link to dashboard nav"
git push -u origin alice/feature/reports-link

# ── Bob ── edits the SAME nav line to add a Settings link
#   (make the file match bob_version.html)
git add base_nav.html
git commit -m "feat: add Settings link to dashboard nav"
git push -u origin bob/fix/nav-settings
```

---

## 3. Alice's PR merges FIRST (no conflict — she was first)

Alice opens her PR → teammate approves → **Squash and merge**. `main` now has
the Reports link. So far so good.

```
   main:  ●── base ──● feat: add Reports link   ← Alice's work is now here
```

---

## 4. Bob syncs main into his branch → 💥 CONFLICT

Bob tries to bring the updated `main` into his branch before his own PR:

```bash
# ── Bob ──
git switch bob/fix/nav-settings
git fetch origin
git merge origin/main
```

Git stops and reports:

```
Auto-merging base_nav.html
CONFLICT (content): Merge conflict in base_nav.html
Automatic merge failed; fix conflicts and then commit the result.
```

Open `base_nav.html` — it now looks like **`conflicted_nav.html`** in this
folder, with `<<<<<<<`, `=======`, `>>>>>>>` markers.

```bash
git status        # shows: both modified: base_nav.html
```

---

## 5. Resolve it (the HUMAN part)

Alice and Bob **talk**: "let's keep both links." Bob edits `base_nav.html` to
match **`resolved_nav.html`** — deleting all three marker lines and keeping the
agreed content:

```html
  <nav class="navbar">
    <a href="/">Home</a> | <a href="/students">Students</a> |
    <a href="/reports">Reports</a> | <a href="/settings">Settings</a>
  </nav>
```

Then finish the merge:

```bash
git add base_nav.html        # tells Git "this conflict is resolved"
git commit                   # Git pre-fills a "Merge branch 'main'..." message — save it
git push
```

> 💡 Tip: `git merge --abort` cancels everything and returns you to the
> pre-merge state if you panic. Nothing is lost.

---

## 6. Bob's PR goes green → merge

With `main` now merged in and the conflict resolved, Bob's PR shows **no
conflicts**. Reviewer approves → **Squash and merge**. Done. 🎉

```
   main:  ●── base ──● Reports (Alice) ──● Settings + resolved (Bob)
                       both links live in the nav
```

Everyone else: `git switch main && git pull` to get the resolved nav.

---

## ✅ What you just learned
- A conflict is **not an error** — it's Git asking a human to make a choice it can't.
- Conflicts happen when **two branches change the same lines**.
- You resolve by **editing the file** (removing markers), then `git add` + `git commit`.
- **Communication** beats tooling: the real fix was Alice & Bob agreeing.
- `git merge --abort` is your safety net.

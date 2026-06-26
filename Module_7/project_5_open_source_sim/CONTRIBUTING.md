# Contributing — example CONTRIBUTING.md

> This is a **typical** CONTRIBUTING.md so you know what real projects ask for.
> When you contribute for real, **read THAT project's file** and follow it
> exactly — conventions differ between projects.

Thanks for your interest in contributing! 🎉 We welcome bug fixes, docs
improvements, and new features.

## Before you start
1. **Search existing issues** — your idea may already be tracked.
2. For anything non-trivial, **open an issue first** to discuss it.
3. Look for the **`good first issue`** label if you're new.
4. **Comment on the issue** to claim it before you start coding.

## Development setup
```bash
git clone https://github.com/<you>/<repo>.git
cd <repo>
python -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest        # make sure tests pass before you change anything
```

## Branch & commit conventions
- Branch from the latest `main`: `git pull upstream main`.
- Name branches `fix/<short-desc>`, `feat/<short-desc>`, or `docs/<short-desc>`.
- Use **Conventional Commits**: `fix: correct off-by-one in pagination`.
- Keep each PR **focused** — one logical change.

## Sign your commits (DCO)
We require the Developer Certificate of Origin. Add a sign-off to every commit:
```bash
git commit -s -m "docs: fix typo in README"
```
This appends `Signed-off-by: Your Name <you@example.com>`.

## Before opening a PR
- [ ] Tests pass locally (`python -m pytest`)
- [ ] New code has tests
- [ ] Docs updated if behaviour changed
- [ ] Commits are signed off (`-s`)
- [ ] Branch is up to date with `upstream/main`

## Opening the PR
- Push to **your fork** (`origin`), open the PR against **this repo's `main`**.
- Fill in the PR template; link the issue (`Closes #123`).
- Be patient and kind — maintainers are volunteers. We'll review as soon as we can.

## Code of Conduct
Be respectful. We follow the Contributor Covenant.

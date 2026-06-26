# 🔵 Project 4 — REST API Repository (Module 5 DRF, CI/CD intro)

**Goal:** take your **Module 5 DRF API** and make it look like a repo a real
company would keep: a thorough README, a `LICENSE`, Swagger docs — and the big
new skill, **CI/CD**. You'll add a **GitHub Actions** workflow that runs your
`APITestCase` suite automatically on every push and PR, and a branch rule so
**a PR can't merge unless the tests pass (green check).**

> **In one sentence:** Project 3 added human reviewers; Project 4 adds a *robot*
> reviewer that runs your tests on every change and blocks broken code.

This is a **demo walkthrough**. Reference copies:
[workflows/tests.yml](workflows/tests.yml) ← **the CI file**,
[README.template.md](README.template.md),
[LICENSE](LICENSE),
[requirements.sample.txt](requirements.sample.txt),
[commit-log.txt](commit-log.txt),
[ci-run-example.txt](ci-run-example.txt).

---

## 📑 Table of Contents
1. [What is CI/CD and why it matters](#-1-what-is-cicd-and-why-it-matters)
2. [Step 1 — Professionalize the repo](#-step-1--professionalize-the-repo)
3. [Step 2 — Add the GitHub Actions workflow](#-step-2--add-the-github-actions-workflow)
4. [Step 3 — Make tests a required merge gate](#-step-3--make-tests-a-required-merge-gate)
5. [Step 4 — Watch it block a bad PR](#-step-4--watch-it-block-a-bad-pr-the-payoff)
6. [Commit standards](#-commit-standards)
7. [Deliverables checklist](#-deliverables-checklist)
8. [Troubleshooting](#-troubleshooting)

---

## 🤖 1. What is CI/CD and why it matters

**CI** = *Continuous Integration*: every time anyone pushes code, a server
automatically installs the project and **runs the tests**. If they fail, everyone
knows in minutes — before the bug reaches `main`.

**CD** = *Continuous Delivery/Deployment*: the same automation can also deploy
passing code. (We focus on CI here; CD is the natural next step.)

```
   WITHOUT CI                          WITH CI (GitHub Actions)
   ──────────                          ────────────────────────
   push code                            push code
      │                                    │
   "did I break anything?" 🤷             GitHub spins up a fresh machine
      │                                    │  ├─ checkout code
   nobody runs the tests                   │  ├─ pip install -r requirements.txt
      │                                    │  └─ python manage.py test
   bug reaches main 💥                     │
                                       ✔ pass → green check, PR can merge
                                       ✗ fail → red X, PR is BLOCKED
```

The green checkmark is the **modern professional standard** — it's the robot
that never forgets to run the tests.

---

## ▶️ Step 1 — Professionalize the repo

Bring your Module 5 API repo up to "others can use this" quality:

- **README** ([README.template.md](README.template.md)) with: what it is, setup
  steps, an **endpoints table**, auth notes, and how to run tests.
- **`.gitignore`** (reuse the production one from Project 2).
- **`requirements.txt`** (see [requirements.sample.txt](requirements.sample.txt)).
- **`LICENSE`** (an [MIT LICENSE](LICENSE) is included — open and friendly).
- **Swagger docs** at `/api/docs/` (Module 5 already wires this with
  `drf-spectacular`) — link it from the README.

Endpoints table — the single most useful thing in an API README:

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| `GET` | `/api/students/` | public | List students (paginated, searchable) |
| `POST` | `/api/students/` | token | Create a student |
| `GET` | `/api/students/{id}/` | public | Retrieve one student |
| `PATCH` | `/api/students/{id}/` | token | Update a student |
| `DELETE` | `/api/students/{id}/` | admin | Delete a student |
| `POST` | `/api/login/` | public | Exchange credentials for a token |
| `GET` | `/api/docs/` | public | Interactive Swagger UI |

---

## ⚙️ Step 2 — Add the GitHub Actions workflow

Create the file **`.github/workflows/tests.yml`** (copy from
[workflows/tests.yml](workflows/tests.yml) in this folder). It tells GitHub:
"on every push and PR, install the project and run the Django tests."

```yaml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: python manage.py test
```

Commit and push it on a branch:

```bash
git switch -c ci/add-actions-workflow
git add .github/workflows/tests.yml
git commit -m "ci: add GitHub Actions test workflow"
git push -u origin ci/add-actions-workflow
```

The moment it lands, open the **Actions** tab — you'll see your suite running on
a fresh Ubuntu machine in the cloud. ([ci-run-example.txt](ci-run-example.txt)
shows what the log looks like.)

```
   push ──▶ GitHub Actions ──▶ ubuntu-latest VM ──▶ pip install ──▶ manage.py test
                                                                      │
                                                          ✔ pass  or  ✗ fail
                                                                      │
                                                       reported back onto the PR
```

---

## 🔒 Step 3 — Make tests a required merge gate

A green check is nice, but the power comes from **requiring** it:

1. **Settings → Branches → Branch ruleset** for `main`.
2. ✅ **Require status checks to pass before merging**.
3. Search for and select the **`test`** check (the job name from the workflow).
4. Save.

Now `main` is doubly protected (from Project 3 + this): a PR needs **1 human
approval AND a green CI check** to merge.

```
   PR ready to merge?
   ├─ 1 approval?        ✔
   ├─ tests green?       ✔   ──▶  "Merge" button is enabled ✅
   └─ either one red?    ✗   ──▶  "Merge" button is BLOCKED 🔒
```

---

## 🎬 Step 4 — Watch it block a bad PR (the payoff)

Prove the gate works — break a test on purpose:

```bash
git switch -c demo/break-a-test
# edit students/api_views.py to introduce a bug (e.g. wrong status code)
git add . && git commit -m "demo: intentionally break student create endpoint"
git push -u origin demo/break-a-test
```

Open the PR. Watch the Actions run go **red ✗**. The merge button is now
**disabled** — GitHub refuses to let broken code into `main`. Revert the change,
push again, watch it go **green ✔**, merge.

That cycle — *red blocks, green allows* — is CI/CD in one sentence, and it's the
habit that separates hobby repos from professional ones.

---

## ✍️ Commit standards

```
feat: add token authentication to student endpoints
feat: add pagination to student list
test: cover student create and delete endpoints
ci:   add GitHub Actions test workflow
docs: add endpoints table and Swagger link to README
chore: add MIT LICENSE
```

See [commit-log.txt](commit-log.txt) for the target history.

---

## ✅ Deliverables checklist

- [ ] Thorough README with setup, **endpoints table**, auth, run-tests, Swagger link.
- [ ] `LICENSE`, `.gitignore`, `requirements.txt` present.
- [ ] `.github/workflows/tests.yml` running `manage.py test` on every push/PR.
- [ ] A **green check** visible on a merged PR.
- [ ] `main` requires the **`test`** status check to pass before merge.
- [ ] You demonstrated CI **blocking** a deliberately-broken PR (red ✗), then green.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| Actions tab shows nothing | The workflow file must be at `.github/workflows/*.yml` on a pushed branch. Check the path. |
| Workflow fails at `pip install` | Make sure `requirements.txt` lists Django + DRF (and `drf-spectacular` for docs). |
| `manage.py test` can't find settings | Add `DJANGO_SETTINGS_MODULE` env or run from the repo root where `manage.py` lives. |
| Tests need a database | SQLite works in CI with zero config — Django creates a temp test DB automatically. |
| Can't select the `test` check in branch rules | It only appears after the workflow has run **at least once**. Push first, then add the rule. |
| Workflow uses secrets (e.g. SECRET_KEY) | Add them in Settings → Secrets and variables → Actions, reference as `${{ secrets.NAME }}`. |

---

➡️ **Next:** [Project 5 — Open Source Contribution](../project_5_open_source_sim/),
the capstone: contribute a real change to a project you **don't own** via the
fork → upstream → PR flow.

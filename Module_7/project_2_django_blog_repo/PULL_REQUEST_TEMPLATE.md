<!--
  Save this as .github/PULL_REQUEST_TEMPLATE.md in your repo.
  GitHub will auto-fill every new PR description with it.
-->

## What does this PR do?
<!-- One or two sentences in plain English. -->


## Why?
<!-- The problem it solves or the feature it adds. Link the issue: Closes #__ -->
Closes #

## How to test it
1.
2.

## Checklist
- [ ] Code runs locally (`python manage.py runserver`) with no errors
- [ ] Migrations included if models changed (`python manage.py makemigrations`)
- [ ] Tests added/updated and passing (`python manage.py test`)
- [ ] No secrets, `db.sqlite3`, or `venv/` in the diff
- [ ] Commit messages follow Conventional Commits (feat/fix/docs/test/...)
- [ ] I self-reviewed the **Files changed** tab

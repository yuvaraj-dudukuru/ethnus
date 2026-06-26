#!/usr/bin/env bash
# build.sh — Render's Build Command. Installs deps, collects static, migrates.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

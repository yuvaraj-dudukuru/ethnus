#!/usr/bin/env bash
# Render runs this once on every deploy (Build Command: ./build.sh).
# Any non-zero exit aborts the deploy, so a broken build never goes live.
set -o errexit   # exit immediately if any command fails

pip install -r requirements.txt
python manage.py collectstatic --noinput   # gather CSS/JS for WhiteNoise
python manage.py migrate                    # apply DB schema to Postgres

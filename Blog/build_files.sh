#!/bin/bash
# Build script for Vercel

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations (optional, since SQLite is file-based)
python manage.py migrate

README.md
# Tailoring Workshop (Django + MySQL + Vanilla JS)

A production-ready starter for a tailoring workshop order system:
- Customer order creation + tracking
- Staff panel with RBAC (roles + permissions)
- SEO: Meta, OG, Twitter, Schema, Canonical, Sitemap, Robots
- Security hardening: secure headers, CSP, rate-limit, secure cookies, etc.

## Quick start

1) Create venv + install:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

Create .env from .env.example

Migrate + create admin + seed roles:

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_roles
python manage.py runserver
Production notes

Set DEBUG=0

Set SITE_URL=https://your-domain.com

Enable HTTPS and set SECURE_SSL_REDIRECT=1

Put behind Nginx/Caddy + TLS


## `LICENSE` (MIT)
```txt
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy...
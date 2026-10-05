# Task Manager — Django CRUD starter

Full-stack Django app: user signup/login, per-user tasks with Create / Read / Update / Delete,
search, status filter, pagination, Bootstrap UI, tests, and ready-to-deploy configs.

## Run locally
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```
Open http://127.0.0.1:8000 and sign up.

## Test
```bash
python manage.py test
```

## Deploy
**Render (easiest):** push to GitHub → Render → New → Blueprint → select repo (uses `render.yaml`).
**Heroku/Railway:** uses `Procfile`; set `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`;
run `python manage.py migrate` and `collectstatic`.
**Docker:** `docker compose up --build` → http://localhost:8000

## Structure
```
config/   settings, urls, wsgi
tasks/    models, forms, views, urls, admin, tests, templates
templates/ base + auth pages     static/ css
```
Env vars: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`, `SECURE_SSL_REDIRECT`.

# KT Public School — Website

Public-facing school website built with Flask, Bootstrap 5, PostgreSQL, and Cloudinary.

## Quick Start (local)

```powershell
cd "D:\KT public school"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python seed.py
python run.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Admin panel

| Route | Description |
|-------|-------------|
| `/admin/login` | Admin sign-in |
| `/admin/` | Dashboard |
| `/admin/notices` | Manage notices |
| `/admin/gallery` | Upload gallery images (Cloudinary) |
| `/admin/inquiries` | View contact/admission submissions |

Set `ADMIN_USERNAME` and `ADMIN_PASSWORD` in your environment. No user database is required.

## Public pages

| Route | Description |
|-------|-------------|
| `/` | Home — hero, highlights, latest notices |
| `/about` | About the school |
| `/admissions` | Admission process + inquiry form |
| `/notices` | All notices |
| `/notices/<id>` | Single notice |
| `/gallery` | Photo gallery |
| `/contact` | Contact form |

## Environment variables

Copy `.env.example` to `.env` and update values:

```
DATABASE_URL=postgresql://user:password@localhost:5432/kt_public_school
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-strong-password
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

Without a `.env` file, the app uses SQLite (`kt_public_school.db`) for local development.

## Deploy to Render

1. Push this repo to GitHub.
2. Create a **Web Service** on Render and connect the repo.
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `gunicorn run:app --bind 0.0.0.0:$PORT`  
   (or leave blank if using the included `Procfile`)
5. Add environment variables:

| Variable | Required | Notes |
|----------|----------|-------|
| `DATABASE_URL` | Yes | Render PostgreSQL connection string |
| `SECRET_KEY` | Yes | Long random string |
| `FLASK_ENV` | Yes | Set to `production` |
| `ADMIN_USERNAME` | Yes | Admin login username |
| `ADMIN_PASSWORD` | Yes | Strong password |
| `CLOUDINARY_CLOUD_NAME` | Yes | From Cloudinary dashboard |
| `CLOUDINARY_API_KEY` | Yes | From Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | Yes | From Cloudinary dashboard |

Render sets `PORT` automatically. Tables are created on startup via `run.py`.

## Database migrations (optional)

```powershell
$env:FLASK_APP = "run.py"
flask db init          # First time only
flask db migrate -m "Initial migration"
flask db upgrade
```

For quick local setup, `python seed.py` creates tables and loads sample data automatically.

## Project structure

See [PROJECT.md](PROJECT.md) for full architecture and planning details.

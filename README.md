# KT Public School — Website

Public-facing school website built with Flask, Bootstrap 5, and PostgreSQL (SQLite for local dev).

## Quick Start

```powershell
cd "D:\KT public school"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Pages

| Route | Description |
|-------|-------------|
| `/` | Home — hero, highlights, latest notices |
| `/about` | About the school |
| `/admissions` | Admission process + inquiry form |
| `/notices` | All notices |
| `/notices/<id>` | Single notice |
| `/gallery` | Photo gallery |
| `/contact` | Contact form |

## Configuration

Copy `.env.example` to `.env` and update values:

```
DATABASE_URL=postgresql://user:password@localhost:5432/kt_public_school
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

Without a `.env` file, the app uses SQLite (`kt_public_school.db`) for local development.

## Database Migrations (PostgreSQL)

```powershell
$env:FLASK_APP = "run.py"
flask db init          # First time only
flask db migrate -m "Initial migration"
flask db upgrade
```

For quick local setup, `python seed.py` creates tables and loads sample data automatically.

## Project Structure

See [PROJECT.md](PROJECT.md) for full architecture and planning details.
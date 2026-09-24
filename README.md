# PC-Repair-Job-Tracker# PC Repair Job Tracker

A small full-stack app to track client repair jobs from intake to completion —
built for my own PC repair and solutions business.

**Status:** Working / deployed
**Stack:** Vue 3 (frontend) + Flask + SQLite (backend)

## What it does

- Log a new repair job: client name, phone, device, and issue description.
- View all jobs in a list, newest first.
- Update a job's status (Received → In Progress → Done).
- Delete a job once it's closed out.

## Why I built it

I run an independent PC repair business and was tracking client jobs
informally (WhatsApp messages, notes). This replaces that with a small,
purpose-built tool — a real problem I actually have, not a tutorial clone.

## Architecture

```
frontend/   Single-file Vue 3 app (CDN build, no bundler needed)
backend/    Flask REST API with SQLite storage
```

**API endpoints:**
| Method | Endpoint | Description |
|---|---|---|
| GET | `/jobs` | List all jobs |
| POST | `/jobs` | Create a job |
| PUT | `/jobs/<id>` | Update a job (status or details) |
| DELETE | `/jobs/<id>` | Delete a job |

## Running locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Runs on `http://127.0.0.1:5000`.

**Frontend:**
Just open `frontend/index.html` in a browser — no build step needed.
Make sure `API_BASE` at the top of the `<script>` block points to your
running backend.

## Deployment

- **Backend:** deployed on Render (free tier) using `gunicorn` (see `Procfile`).
- **Frontend:** deployed as a static site on Vercel/Netlify — update
  `API_BASE` in `index.html` to the live backend URL before deploying.

## Possible next steps

- Add authentication so only I can access my own job list.
- Add search/filter by status or client name.
- Move from SQLite to Postgres for a persistent production database
  (Render's free tier SQLite storage is not guaranteed to persist across
  redeploys).

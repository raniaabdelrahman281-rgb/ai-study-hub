# 🎓 AI Study Hub

A Django (MVT) web application that helps students organize tasks, notes, and
learning resources, with an integrated AI assistant for summarizing notes,
generating quizzes/flashcards, and explaining programming errors.

Built for the course project brief: Django MVT only (no DRF, no frontend
frameworks), PostgreSQL database, vanilla HTML/CSS/JS.

## Features

- **Authentication**: register, login, logout, profile page, change password,
  email verification, password reset
- **Dashboard**: totals for tasks/notes/resources, upcoming tasks, recent
  activity feed, a Chart.js chart of tasks by priority
- **Study Planner**: subjects, tasks with priority/due date/complete-toggle
  (AJAX, no page reload)
- **Notes**: full CRUD, categories (many-to-many), server-side search, and a
  JavaScript live-search box backed by a small JSON endpoint (no DRF)
- **Resources**: full CRUD with title/description/link/type and optional
  thumbnail image
- **AI Assistant** (`ai_assistant` app): chat, summarize a note, generate a
  quiz, generate flashcards, explain a programming error — all going through
  one small `services.py` wrapper around an OpenAI-compatible chat
  completions API
- **Extras**: dark mode, pagination, image upload, responsive layout

## Project structure

```
ai_study_hub/
├── config/            # settings, root urls, wsgi/asgi
├── accounts/          # Profile model, auth views/forms/templates
├── planner/            # Subject, Task, StudySession
├── notes/              # Note, Category
├── resources/          # Resource
├── ai_assistant/       # AIConversation, AI service wrapper, feature views
├── dashboard/          # aggregated home view
├── templates/          # base.html + shared partials
├── static/             # css/js
└── media/              # user-uploaded avatars & thumbnails
```

## Database (ERD)

9 tables total, with 1:N relationships from `User` down through `Subject`,
`Task`, `StudySession`, `Note`, `Category`, `Resource`, `AIConversation`, a
1:1 `User ↔ Profile`, and an M:N between `Note` and `Category`. See
`erd.png` in this deliverable for the full diagram.

## Setup

### 1. Clone & create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your PostgreSQL credentials and (optionally) an AI
provider key:
```
DB_NAME=ai_study_hub
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

AI_API_KEY=sk-...
AI_API_URL=https://api.openai.com/v1/chat/completions
AI_MODEL=gpt-4o-mini
```
> The AI features work with any OpenAI-compatible `/chat/completions`
> endpoint — just change `AI_API_URL` and `AI_MODEL` for a different
> provider. Without a key configured, the AI pages still load and simply
> show a friendly error instead of crashing.

### 3. Create the PostgreSQL database
```sql
CREATE DATABASE ai_study_hub;
```

### 4. Run migrations & create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the dev server
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000

> For a quick smoke test without PostgreSQL installed, you can set
> `DB_ENGINE=sqlite` as an environment variable before running the commands
> above — the project will fall back to a local `db.sqlite3` file.

## AI feature notes

`ai_assistant/services.py` is the single place that talks to the external
AI API. Each feature (summarize, quiz, flashcards, explain-error, chat) is a
thin function that builds a system prompt and calls the shared `call_ai()`
helper — swap providers or prompts there without touching the views.

## Deliverables checklist

- [x] Complete source code
- [x] `requirements.txt`
- [x] `.env.example`
- [x] `README.md`
- [x] ERD (`erd.png`)
- [x] Screenshots (`screenshots/`)
- [ ] PostgreSQL database backup — generate with:
      `pg_dump -U postgres ai_study_hub > db_backup.sql` once you have real
      data in a Postgres instance
- [ ] Push to GitHub

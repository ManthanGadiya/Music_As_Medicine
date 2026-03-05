# Music Therapy System

Music Therapy System is a full-stack application for managing therapy participants, music-assisted sessions, pre/post assessments, and participant progress insights.

## Tech Stack

- Frontend: HTML, CSS, Vanilla JavaScript
- Backend: FastAPI (Python)
- Database: SQLite

## Project Structure

```text
Music_As_Medicine/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── data/
│   │   └── seed_data.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── participant_routes.py
│   │   ├── music_routes.py
│   │   └── session_routes.py
│   ├── schemas/
│   ├── services/
│   ├── static/
│   │   ├── css/styles.css
│   │   └── js/
│   │       ├── api.js
│   │       ├── auth.js
│   │       ├── participants.js
│   │       ├── sessions.js
│   │       ├── music.js
│   │       ├── reports.js
│   │       └── ui.js
│   └── templates/
│       ├── index.html
│       ├── login.html
│       ├── signup.html
│       ├── dashboard.html
│       ├── participants.html
│       ├── participant_profile.html
│       ├── music_library.html
│       ├── therapy_session.html
│       ├── pre_assessment.html
│       ├── post_feedback.html
│       ├── progress_report.html
│       └── hospital_network.html
├── scripts/
│   ├── create_database.py
│   ├── load_music_data.py
│   ├── generate_reports.py
│   └── refresh_meaningful_data.py
├── music_therapy.db
├── run.py
├── requirements.txt
└── README.md
```

## Installation

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

Initialize database schema:

```bash
python scripts/create_database.py
```

Optional data scripts:

```bash
python -m app.data.seed_data
python -m scripts.refresh_meaningful_data
```

`refresh_meaningful_data.py` updates sample records and ensures each participant has 4 sessions with both pre- and post-session records.

## Run the Application

```bash
python run.py
```

Server starts at:

- API docs: `http://127.0.0.1:8000/docs`
- App pages: `http://127.0.0.1:8000/login` (default redirect from `/`)

## API Endpoints (Implemented)

Base prefix: `/api/v1`

- `POST /auth/login`
- `POST /participants`
- `GET /participants`
- `GET /participants/{participant_id}`
- `GET /participants/{participant_id}/sessions`
- `GET /participants/{participant_id}/progress`
- `GET /music`
- `POST /music`
- `POST /sessions`
- `GET /sessions/{session_id}`
- `POST /sessions/{session_id}/pre-assessment`
- `POST /sessions/{session_id}/feedback`

## Frontend Routes

- `/home` or `/index` - Landing page
- `/login` - Login
- `/signup` - Signup-style screen
- `/dashboard` - Main control panel
- `/participants` - Participant management
- `/participant-profile?id=<participant_id>` - Participant profile
- `/music-library` - Music tracks
- `/therapy-session` - Start session
- `/pre-assessment` - Pre-session assessment
- `/post-feedback` - Post-session feedback
- `/progress-report` - Analytics and reports
- `/hospital-network` - Hospital cards/map placeholder

## Workflow

1. Login
2. Open Dashboard
3. Create/select participant
4. Start therapy session
5. Fill pre-assessment
6. Fill post-feedback
7. Review progress report

The UI auto-redirect chain is implemented:

- Start Session -> Pre Assessment -> Post Feedback -> Progress Report

## Authentication Note

The provided schema does not include a password column in `Therapists`, and the documented API only defines `POST /auth/login`.

Current behavior:

- Login validates therapist email from `Therapists.contact_email`
- Uses documented sample password (`password123`) for authentication check

Signup UI exists for user flow consistency, but there is no dedicated signup backend endpoint in the required API spec.

## Testing

Basic endpoint and module checks can be run with:

```bash
python -m compileall app scripts run.py main.py
pytest
```

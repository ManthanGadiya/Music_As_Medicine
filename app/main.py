from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import API_PREFIX
from app.data.seed_data import seed_therapist
from app.database import initialize_database
from app.routes.auth_routes import router as auth_router
from app.routes.music_routes import router as music_router
from app.routes.participant_routes import router as participant_router
from app.routes.session_routes import router as session_router


app = FastAPI(title="Music Therapy System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def startup_event() -> None:
    initialize_database()
    seed_therapist()


app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(participant_router, prefix=API_PREFIX)
app.include_router(music_router, prefix=API_PREFIX)
app.include_router(session_router, prefix=API_PREFIX)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/login")


@app.get("/login", include_in_schema=False)
def login_page() -> FileResponse:
    return FileResponse("app/templates/login.html")


@app.get("/dashboard", include_in_schema=False)
def dashboard_page() -> FileResponse:
    return FileResponse("app/templates/dashboard.html")


@app.get("/participants", include_in_schema=False)
def participants_page() -> FileResponse:
    return FileResponse("app/templates/participants.html")


@app.get("/participant-profile", include_in_schema=False)
def participant_profile_page() -> FileResponse:
    return FileResponse("app/templates/participant_profile.html")


@app.get("/music-library", include_in_schema=False)
def music_library_page() -> FileResponse:
    return FileResponse("app/templates/music_library.html")


@app.get("/therapy-session", include_in_schema=False)
def therapy_session_page() -> FileResponse:
    return FileResponse("app/templates/therapy_session.html")


@app.get("/pre-session-assessment", include_in_schema=False)
def pre_assessment_page() -> FileResponse:
    return FileResponse("app/templates/pre_session_assessment.html")


@app.get("/post-session-feedback", include_in_schema=False)
def post_feedback_page() -> FileResponse:
    return FileResponse("app/templates/post_session_feedback.html")


@app.get("/progress-report", include_in_schema=False)
def progress_report_page() -> FileResponse:
    return FileResponse("app/templates/progress_report.html")

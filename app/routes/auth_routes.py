from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.therapist_schema import LoginRequest, LoginResponse
from app.utils.auth_utils import build_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT therapist_id, name, contact_email FROM Therapists WHERE contact_email = ?",
            (payload.email,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if payload.password != "password123":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = build_access_token(row["therapist_id"], row["contact_email"])
    return LoginResponse(
        access_token=token,
        therapist_id=row["therapist_id"],
        name=row["name"],
    )

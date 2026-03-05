from fastapi import HTTPException


def validate_mood_scale(value: int, field_name: str) -> None:
    if value < 1 or value > 10:
        raise HTTPException(status_code=400, detail=f"{field_name} must be between 1 and 10")

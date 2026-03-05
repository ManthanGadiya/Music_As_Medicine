from datetime import datetime, timezone


def build_access_token(therapist_id: int, email: str) -> str:
    # Lightweight token format for demo purposes.
    issued = int(datetime.now(tz=timezone.utc).timestamp())
    return f"therapist-{therapist_id}:{email}:{issued}"

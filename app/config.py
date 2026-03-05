from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "music_therapy.db"
API_PREFIX = "/api/v1"

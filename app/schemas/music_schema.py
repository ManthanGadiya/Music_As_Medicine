from pydantic import BaseModel, Field


class MusicCreate(BaseModel):
    title: str = Field(max_length=100)
    genre: str = Field(max_length=50)
    instrument: str = Field(max_length=50)
    tempo: float
    frequency_range: str = Field(max_length=50)
    duration_sec: int
    file_path: str


class MusicOut(BaseModel):
    music_id: int
    title: str
    genre: str
    instrument: str
    tempo: float
    frequency_range: str
    duration_sec: int
    file_path: str

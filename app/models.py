from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class Detection(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    detected_object: str = Field(index=True)
    score: float = Field(index=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    image_path: str
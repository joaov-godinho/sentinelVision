from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Detection

# Criamos o router. O 'prefix' evita repetir /detections em cada rota.
router = APIRouter(prefix="/detections", tags=["Detections"])

@router.post("/", response_model=Detection)
def create_detection(detection: Detection, session: Session = Depends(get_session)):
    # 1. Add the new object in the session
    session.add(detection)

    # 2. Commit the changes to the database
    session.commit()

    # 3. Refresh the object to get updated data (e.g., auto-generated ID)
    session.refresh(detection)
    return detection

@router.get("/", response_model=List[Detection])
def read_detections(session: Session = Depends(get_session)):
    return session.exec(select(Detection)).all()

@router.get("/paginated", response_model=List[Detection])
def read_detections_paginated(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=1000)
) -> list[Detection]:
    # Query the database for detections with pagination
    statement = select(Detection).offset(offset).limit(limit)
    detections = session.exec(statement).all()
    return detections
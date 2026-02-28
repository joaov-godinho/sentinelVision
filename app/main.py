from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sqlmodel import Session
from app.database import create_db_and_tables, get_session
from app.models import Detection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: Create the database and tables
    create_db_and_tables()
    
    yield # Heres the API is running

    # Shutdown code (if needed) can be added here
    print("Shutting down the Sentinel Vision API...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sentinel Vision API!"}

@app.post("/detections/", response_model=Detection)
def create_detection(detection: Detection, session: Session = Depends(get_session)):
    # 1. Add the new object in the session
    session.add(detection)

    # 2. Commit the changes to the database
    session.commit()

    # 3. Refresh the object to get updated data (e.g., auto-generated ID)
    session.refresh(detection)

    return detection

@app.get("/detections/")
def read_detections(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=1000)
) -> list[Detection]:
    # Query the database for detections with pagination
    detections = session.query(Detection).offset(offset).limit(limit).all()
    return detections
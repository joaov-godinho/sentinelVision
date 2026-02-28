from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routers import detections

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: Create the database and tables
    create_db_and_tables()
    
    yield # Heres the API is running

    # Shutdown code (if needed) can be added here
    print("Shutting down the Sentinel Vision API...")

app = FastAPI(lifespan=lifespan)

app.include_router(detections.router)

@app.get("/")
def health_check():
    return {"status": "SentinelVision API is modular and healthy!"}
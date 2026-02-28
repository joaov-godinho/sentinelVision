import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the connection with the database
engine = create_engine(DATABASE_URL, echo=True) # Set echo to True to see the generated SQL statements

def create_db_and_tables():
    #See all the models and create the tables in the database
    SQLModel.metadata.create_all(engine)

def get_session():
    #Generate the sessions to FastAPI routes
    with Session(engine) as session:
        yield session
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemyseeder import ResolvingSeeder
from .database import SessionLocal, engine
from . import models
from src.schemas import Student

def is_database_empty(session):
    return session.query(models.Students).first() is None

def seed_database():
    with SessionLocal() as session:
        if is_database_empty(session):
            ResolvingSeeder(session).load_entities_from_json_file("src/seed.json")
            session.commit()
            print("Database seeded successfully.")
        else:
            print("Database already contains data. Skipping seeding.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    seed_database()
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=Student)
def read_root(db: Session = Depends(get_db)):
    return db.query(models.Students).first()
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemyseeder import ResolvingSeeder
from .database import SessionLocal

from . import models
from .database import engine

from src.schemas import Student

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

with SessionLocal() as session:
    ResolvingSeeder(session).load_entities_from_json_file("src/seed.json")
    session.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=Student)
def read_root(db: Session = Depends(get_db)):
    return db.query(models.Students).first()
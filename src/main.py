from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemyseeder import ResolvingSeeder
from .database import SessionLocal

from . import models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

ResolvingSeeder(SessionLocal()).load_entities_from_json_file("src/seed.json")
SessionLocal().commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}
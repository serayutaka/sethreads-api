from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Response, status
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemyseeder import ResolvingSeeder

from .database import SessionLocal, engine
from . import models, schemas

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

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

@app.get("/")
def read_root():
    return {"Hello": "Hackers"}

def hashing(password: str):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

@app.post("/sign-up", status_code=status.HTTP_201_CREATED)
def signup(response: Response, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    try:
        student = student.model_dump()
        db_student = db.query(models.Students).filter(models.Students.student_id == student["student_id"]).first()
        print(db_student.hashed_password)
        
        if db_student.hashed_password != None:
            response.status_code = status.HTTP_409_CONFLICT
            return {"error": "Student already signed up"}
        
        hashed_password = hashing(student["password"])
        db_student.hashed_password = hashed_password
        db.commit()
        
        response.status_code = status.HTTP_201_CREATED
        return {"successful": "Student sign up successfully"}
    except(Exception):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Student not found"}

class Signin(BaseModel):
    student_id: str
    password: str
@app.post("/sign-in", status_code=status.HTTP_200_OK)
def signin(response: Response, signin: Signin, db: Session = Depends(get_db)):
    signin = signin.model_dump()
    student_id = signin["student_id"]
    password = signin["password"]
    try:
        student = db.query(models.Students).filter(models.Students.student_id == student_id).first()
        if bcrypt.checkpw(password.encode("utf-8"), student.hashed_password) == False:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"error": "Incorrect password"}
        
        payload = {
            "student_id": student_id,
            "exp": datetime.now(timezone.utc) + timedelta(hours=10),
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, "mysecretpassword", algorithm="HS256")
        
        return {"successful": "Student sign in successfully", "token": token}
    except(Exception):
        return {"error": Exception}

class verify_token(BaseModel):
    token: str

@app.post("/verify", status_code=status.HTTP_200_OK)
def verify(response: Response, verify: verify_token, db: Session = Depends(get_db)):
    verify = verify.model_dump()
    token = verify["token"]
    
    try:
        payload = jwt.decode(token, "mysecretpassword", algorithms=["HS256"])
        return {"successful": "Token verified"}
    except jwt.ExpiredSignatureError:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "Token expired"}
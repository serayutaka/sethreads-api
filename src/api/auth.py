from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Response, APIRouter, Header
from pydantic import BaseModel
from typing import Annotated 

from .. import models, schemas
from ..common import get_db

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone


router = APIRouter()

def hashing(password: str):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")

@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
def signup(response: Response, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    try:
        db_student = db.query(models.Students).filter(models.Students.id == student.id).first()
        
        if db_student.hashed_password != None:
            response.status_code = status.HTTP_409_CONFLICT
            return {"error": "Student already signed up"}
        
        hashed_password = hashing(student.password)
        db_student.hashed_password = hashed_password
        db.commit()

        payload = {
            "sub": { "student_id" : student.id },
            "exp": datetime.now(timezone.utc) + timedelta(hours=10),
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, "mysecretpassword", algorithm="HS256")
        
        response.status_code = status.HTTP_201_CREATED
        return {"successful": "Student sign up successfully", "token": token}
    except(Exception):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Student not found"}

class Signin(BaseModel):
    student_id: str
    password: str
@router.post("/sign-in", status_code=status.HTTP_200_OK)
def signin(response: Response, signin: Signin, db: Session = Depends(get_db)):
    student_id = signin.student_id
    password = signin.password
    if (student_id == "admin" and password == "admin"):
        payload = {
            "sub": { "student_id" : student_id },
            "exp": datetime.now(timezone.utc) + timedelta(hours=10),
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, "mysecretpassword", algorithm="HS256")
        
        return {"successful": "Admin sign in successfully", "token": token, "admin": True}
    try:
        student = db.query(models.Students).filter(models.Students.id == student_id).first()
        if bcrypt.checkpw(password.encode("utf-8"), str.encode(student.hashed_password)) == False:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"error": "Incorrect password"}

        payload = {
            "sub": { "student_id" : student_id },
            "exp": datetime.now(timezone.utc) + timedelta(hours=10),
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, "mysecretpassword", algorithm="HS256")
        
        return {"successful": "Student sign in successfully", "token": token}
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Student not found"}
        

@router.get("/verify", status_code=status.HTTP_200_OK)
def verify(response: Response, x_token: Annotated[str | None, Header()] = None):
    try:
        payload = jwt.decode(x_token, "mysecretpassword", algorithms=["HS256"])
        return {"successful": "Token verified", "student_id": payload["sub"]["student_id"]}
    except jwt.ExpiredSignatureError:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "Invalid token"}
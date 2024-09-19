from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemyseeder import ResolvingSeeder

from ..database import Base
from ..app import app, is_database_empty
from ..common import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def seed_database():
    with TestingSessionLocal() as session:
        if is_database_empty(session):
            ResolvingSeeder(session).load_entities_from_json_file("src/seed.json")
            session.commit()
            print("Database seeded successfully.")
        else:
            print("Database already contains data. Skipping seeding.")

def setup_module(module):
    Base.metadata.create_all(bind=engine)
    seed_database()

def teardown_module(module):
    Base.metadata.drop_all(bind=engine)

def test_signup():
    response = client.post("/sign-up", json={"student_id": "66011192", "password": "mysecretpassword"})
    assert response.status_code == 201
    assert response.json() == {"successful": "Student sign up successfully"}

def test_signup_conflict():
    response = client.post("/sign-up", json={"student_id": "66011192", "password": "mysecretpassword"})
    assert response.status_code == 409
    assert response.json() == {"error": "Student already signed up"}

def test_signup_not_found():
    response = client.post("/sign-up", json={"student_id": "69889721", "password": "mysecretpassword"})
    assert response.status_code == 404
    assert response.json() == {"error": "Student not found"}

def test_signin():
    response = client.post("/sign-in", json={"student_id": "66011192", "password": "mysecretpassword"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_signin_unauthorized():
    response = client.post("/sign-in", json={"student_id": "66011192", "password": "mysecretpassword1"})
    assert response.status_code == 401
    assert response.json() == {"error": "Incorrect password"}

def test_signin_not_found():
    response = client.post("/sign-in", json={"student_id": "69889721", "password": "mysecret"})
    assert response.status_code == 404
    assert response.json() == {"error": "Student not found"}

def get_token():
    response = client.post("/sign-in", json={"student_id": "66011192", "password": "mysecretpassword"})
    return response.json()["token"]

def test_read_student_invalid_token():
    response = client.get("api/student/get-info?student_id=66011192", headers={"x-token": get_token() + "invalid"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid token"}

def test_read_student():
    response = client.get("api/student/get-info?student_id=66011192", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "student_id": "66011192",
        "name": "Rachata",
        "surname": "Phondi",
        "year": 2,
        "is_ta": None,
        "picture": None,
        "ta_course_id": None,
        "registered_courses": [
            {
            "course_id": "01006719",
            "name": "PROBABILITY AND STATISTICS",
            "student_id": 66011192,
            "forums": []
            },
            {
            "course_id": "01286213",
            "name": "COMPUTER ARCHITECTURE AND ORGANIZATION",
            "student_id": 66011192,
            "forums": []
            },
            {
            "course_id": "01286222",
            "name": "DATA STRUCTURES AND ALGORITHMS",
            "student_id": 66011192,
            "forums": []
            },
            {
            "course_id": "01286233",
            "name": "WEB PROGRAMMING",
            "student_id": 66011192,
            "forums": []
            },
            {
            "course_id": "96644042",
            "name": "PROFESSIONAL COMMUNICATION AND PRESENTATION",
            "student_id": 66011192,
            "forums": []
            }
        ],
        "posted": [],
        "comment": [],
        "reply": []
    }
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

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Hackers"}
    
def get_token():
    response = client.post("/sign-in", json={"student_id": "66011192", "password": "mysecretpassword"})
    return response.json()["token"]

def test_signup():
    response = client.post("/sign-up", json={"student_id": "66011192", "password": "mysecretpassword"})
    assert response.status_code == 201
    assert "successful" in response.json()
    assert "token" in response.json()

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

def test_read_student_invalid_token():
    response = client.get("api/student/get-info?student_id=66011192", headers={"x-token": get_token() + "invalid"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid token"}

def test_verify_token():
    response = client.get("/verify", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {"successful": "Token verified", "student_id": "66011192"}

def test_verify_token_invalid():
    response = client.get("/verify", headers={"x-token": get_token() + "invalid"})
    assert response.status_code == 401
    assert response.json() == {"error": "Invalid token"}

def test_read_student():
    response = client.get("api/student/get-info?student_id=66011192", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "student_id": "66011192",
        "name": "Rachata",
        "surname": "Phondi",
        "year": 2,
        "is_ta": None,
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

def test_read_student_not_found():
    response = client.get("api/student/get-info?student_id=69889721", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}

def test_read_ta_courses():
    response = client.get("api/student/get-courses?course_id=01286213", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "course_id": "01286213",
        "name": "COMPUTER ARCHITECTURE AND ORGANIZATION",
        "student_id": 66011525,
        "forums": []
    }

def test_read_ta_courses_not_found():
    response = client.get("api/student/get-courses?course_id=01286214", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}

def test_create_thread():
    response = client.post("api/thread/create-thread", json={
        "course_id": "01286213",
        "create_by": "66011192",
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})
    assert response.status_code == 201
    assert response.json() == {
        "course_id": "01286213",
        "id": 1,
        "create_by": "66011192",
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00",
        "comments": [],
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
            }
        }
    
def create_thread():
    response = client.post("api/thread/create-thread", json={
        "course_id": "01286213",
        "create_by": "66011192",
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})


def test_read_thread_by_course_id():
    create_thread()
    response = client.get("api/thread/get-all?course_id=01286213&limit=2&offset=0", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == [
        {
            "course_id": "01286213",
            "id": 1,
            "create_by": "66011192",
            "title": "<h2>This is title</h2>",
            "body": "<p>This is body</p>",
            "is_highlight": False,
            "create_at": "2021-09-01 12:00:00",
            "comments": [],
            "author": {
                "student_id": "66011192",
                "name": "Rachata",
                "surname": "Phondi",
                "year": 2,
                "is_ta": None,
                "ta_course_id": None
            }
        },
        {
            "course_id": "01286213",
            "id": 2,
            "create_by": "66011192",
            "title": "<h2>This is title</h2>",
            "body": "<p>This is body</p>",
            "is_highlight": False,
            "create_at": "2021-09-01 12:00:00",
            "comments": [],
            "author": {
                "student_id": "66011192",
                "name": "Rachata",
                "surname": "Phondi",
                "year": 2,
                "is_ta": None,
                "ta_course_id": None
            }
        }
    ]

def test_read_thread_by_course_id_not_found():
    response = client.get("api/thread/get-all?course_id=01286214&limit=2&offset=0", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}

def test_read_thread_by_id():
    response = client.get("api/thread/get-thread?thread_id=1&course_id=01286213", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "course_id": "01286213",
        "id": 1,
        "create_by": "66011192",
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00",
        "comments": [],
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def test_read_thread_by_id_not_found():
    response = client.get("api/thread/get-thread?thread_id=3&course_id=01286213", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Thread not found"}

def test_read_thread_by_id_and_course_id_not_found():
    response = client.get("api/thread/get-thread?thread_id=2&course_id=01286214", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Thread not found"}

def test_update_thread():
    response = client.put("api/thread/update-thread?thread_id=1", json={
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00"
    }

def test_update_thread_not_found():
    response = client.put("api/thread/update-thread?thread_id=3", json={
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Thread not found"}

def test_update_thread_highlight():
    response = client.put("api/thread/update-is-highlight?thread_id=2", json={}, headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": True,
        "create_at": "2021-09-01 12:00:00"
    }

def test_delete_thread():
    response = client.delete("api/thread/delete-thread?thread_id=2", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {"message": "Thread deleted successfully"}

def test_delete_thread_not_found():
    response = client.delete("api/thread/delete-thread?thread_id=3", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Thread not found"}

def test_create_comment():
    response = client.post("api/comment/create-comment", json={
        "comment_from": 1,
        "comment_data": "<p>This is comment</p>",
        "posted_by": "66011192",
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})
    assert response.status_code == 201
    assert response.json() == {
        "comment_from": 1,
        "id": 1,
        "comment_data": "<p>This is comment</p>",
        "create_at": "2021-09-01 12:00:00",
        "subcomments": [],
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def create_comment():
    response = client.post("api/comment/create-comment", json={
        "comment_from": 1,
        "comment_data": "<p>This is comment</p>",
        "posted_by": "66011192",
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})

def test_read_comment_by_thread_id():
    create_comment()
    response = client.get("api/comment/get-comments?thread_id=1&limit=2&offset=0", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == [
        {
            "comment_from": 1,
            "id": 1,
            "comment_data": "<p>This is comment</p>",
            "create_at": "2021-09-01 12:00:00",
            "subcomments": [],
            "author": {
                "student_id": "66011192",
                "name": "Rachata",
                "surname": "Phondi",
                "year": 2,
                "is_ta": None,
                "ta_course_id": None
            }
        },
        {
            "comment_from": 1,
            "id": 2,
            "comment_data": "<p>This is comment</p>",
            "create_at": "2021-09-01 12:00:00",
            "subcomments": [],
            "author": {
                "student_id": "66011192",
                "name": "Rachata",
                "surname": "Phondi",
                "year": 2,
                "is_ta": None,
                "ta_course_id": None
            }
        }
    ]

def test_read_thread_with_comment():
    response = client.get("api/thread/get-thread?thread_id=1&course_id=01286213", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "course_id": "01286213",
        "id": 1,
        "create_by": "66011192",
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00",
        "comments": [
            {
                "comment_from": 1,
                "id": 1,
            },
            {
                "comment_from": 1,
                "id": 2,
            }
        ],
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def test_read_comment_by_thread_id_not_found():
    response = client.get("api/comment/get-comments?thread_id=2&limit=2&offset=0", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Thread not found"}

def test_update_comment():
    response = client.put("api/comment/update-comment?comment_id=1", json={
        "comment_data": "<p>Update comment</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
            "comment_from": 1,
            "id": 1,
            "comment_data": "<p>Update comment</p>",
            "create_at": "2021-09-01 12:00:10",
            "subcomments": [],
            "author": {
                "student_id": "66011192",
                "name": "Rachata",
                "surname": "Phondi",
                "year": 2,
                "is_ta": None,
                "ta_course_id": None
            }
        }
    
def test_update_comment_not_found():
    response = client.put("api/comment/update-comment?comment_id=3", json={
        "comment_data": "<p>Update comment</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}

def test_delete_comment():
    response = client.delete("api/comment/delete-comment?comment_id=2", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {"message": "Comment deleted successfully"}

def test_delete_comment_not_found():
    response = client.delete("api/comment/delete-comment?comment_id=3", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}

def test_create_subcomment():
    response = client.post("/api/comment/create-subcomment?", json={
        "reply_of": 1,
        "posted_by": "66011192",
        "reply_data": "<p>u are gay</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})
    assert response.status_code == 201
    assert response.json() == {
        "reply_of": 1,
        "posted_by": "66011192",
        "reply_data": "<p>u are gay</p>",
        "create_at": "2021-09-01 12:00:10",
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def create_sub_comment():
    response = client.post("/api/comment/create-subcomment", json={
        "reply_of": 1,
        "posted_by": "66011192",
        "reply_data": "<p>this is another reply comment</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})
    

def test_create_subcomment_not_found():
    response = client.post("/api/comment/create-subcomment?", json={
        "reply_of": 3,
        "posted_by": "66011192",
        "reply_data": "<p>this is another reply comment</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}

def test_update_subcomment():
    response = client.put("api/comment/update-subcomment?subcomment_id=1", json={
        "reply_data": "<p>Update subcomment</p>",
        "create_at": "2021-09-01 12:00:12"
    }, headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "reply_of": 1,
        "posted_by": "66011192",
        "reply_data": "<p>Update subcomment</p>",
        "create_at": "2021-09-01 12:00:12",
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def test_update_subcomment_not_found():
    response = client.put("api/comment/update-subcomment?subcomment_id=3", json={
        "reply_data": "<p>Update subcomment</p>",
        "create_at": "2021-09-01 12:00:12"
    }, headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Subcomment not found"}

def test_delete_subcomment():
    response = client.delete("api/comment/delete-subcomment?subcomment_id=1", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {"successful": "Subcomment deleted successfully"}

def test_delete_subcomment_not_found():
    response = client.delete("api/comment/delete-subcomment?subcomment_id=3", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Subcomment not found"}

def test_create_home_thread():
    response = client.post("api/home/create-thread", json={
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00",
        "create_by": "66011192"
    }, headers={"x-token": get_token()})
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "create_by": "66011192",
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00",
        "comments": [],
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def create_home_thread():
    response = client.post("api/home/create-thread", json={
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00",
        "create_by": "66011192"
    }, headers={"x-token": get_token()})

def test_read_home_thread():
    create_home_thread()
    response = client.get("api/home/get-all?limit=2&offset=0", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "create_by": "66011192",
            "title": "<h2>This is title</h2>",
            "body": "<p>This is body</p>",
            "is_highlight": False,
            "create_at": "2021-09-01 12:00:00",
            "comments": [],
            "author": {
                "student_id": "66011192",
                "name": "Rachata",
                "surname": "Phondi",
                "year": 2,
                "is_ta": None,
                "ta_course_id": None
            }
        },
        {
            "id": 2,
            "create_by": "66011192",
            "title": "<h2>This is title</h2>",
            "body": "<p>This is body</p>",
            "is_highlight": False,
            "create_at": "2021-09-01 12:00:00",
            "comments": [],
            "author": {
                "student_id": "66011192",
                "name": "Rachata",
                "surname": "Phondi",
                "year": 2,
                "is_ta": None,
                "ta_course_id": None
            }
        }
    ]

def test_read_home_thread_not_found():
    response = client.get("api/home/get-all?limit=2&offset=10", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == []

def test_read_home_thread_by_id():
    response = client.get("api/home/get-thread?thread_id=1", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "create_by": "66011192",
        "title": "<h2>This is title</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00",
        "comments": [],
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def test_read_home_thread_by_id_not_found():
    response = client.get("api/home/get-thread?thread_id=3", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Thread not found"}

def test_update_home_thread():
    response = client.put("api/home/update-thread?thread_id=1", json={
        "title": "<h2>This is title update</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "title": "<h2>This is title update</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00"
    }

def test_update_home_thread_not_found():
    response = client.put("api/home/update-thread?thread_id=3", json={
        "title": "<h2>This is title update</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Thread not found"}

def test_delete_home_thread():
    response = client.delete("api/home/delete-thread?thread_id=2", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {"message": "Thread deleted successfully"}

def test_delete_home_thread_not_found():
    response = client.delete("api/home/delete-thread?thread_id=3", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Thread not found"}

def test_create_home_comment():
    response = client.post("api/home-comment/create-comment", json={
        "comment_from": 1,
        "comment_data": "<p>This is comment</p>",
        "posted_by": "66011192",
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})
    assert response.status_code == 201
    assert response.json() == {
        "comment_from": 1,
        "id": 1,
        "comment_data": "<p>This is comment</p>",
        "create_at": "2021-09-01 12:00:00",
        "subcomments": [],
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def create_home_comment():
    response = client.post("api/home-comment/create-comment", json={
        "comment_from": 1,
        "comment_data": "<p>This is comment</p>",
        "posted_by": "66011192",
        "create_at": "2021-09-01 12:00:00"
    }, headers={"x-token": get_token()})

def test_read_home_comment_by_thread_id():
    create_home_comment()
    response = client.get("api/home-comment/get-comments?home_id=1&limit=2&offset=0", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == [
        {
            "comment_from": 1,
            "id": 1,
            "comment_data": "<p>This is comment</p>",
            "create_at": "2021-09-01 12:00:00",
            "subcomments": [],
            "author": {
                "student_id": "66011192",
                "name": "Rachata",
                "surname": "Phondi",
                "year": 2,
                "is_ta": None,
                "ta_course_id": None
            }
        },
        {
            "comment_from": 1,
            "id": 2,
            "comment_data": "<p>This is comment</p>",
            "create_at": "2021-09-01 12:00:00",
            "subcomments": [],
            "author": {
                "student_id": "66011192",
                "name": "Rachata",
                "surname": "Phondi",
                "year": 2,
                "is_ta": None,
                "ta_course_id": None
            }
        }
    ]

def test_read_home_thread_with_comment():
    response = client.get("api/home/get-thread?thread_id=1", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "<h2>This is title update</h2>",
        "body": "<p>This is body</p>",
        "is_highlight": False,
        "create_at": "2021-09-01 12:00:00",
        "create_by": "66011192",
        "comments": [
            {
                "comment_from": 1,
                "id": 1,
            },
            {
                "comment_from": 1,
                "id": 2,
            }
        ],
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def test_read_home_comment_by_thread_id_not_found():
    response = client.get("api/home-comment/get-comments?home_id=2&limit=2&offset=0", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "No comments found"}

def test_update_home_comment():
    response = client.put("api/home-comment/update-comment?comment_id=1", json={
        "comment_data": "<p>Update comment</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "comment_from": 1,
        "id": 1,
        "comment_data": "<p>Update comment</p>",
        "create_at": "2021-09-01 12:00:10",
        "subcomments": [],
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def test_update_home_comment_not_found():
    response = client.put("api/home-comment/update-comment?comment_id=3", json={
        "comment_data": "<p>Update comment</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}

def test_delete_home_comment():
    response = client.delete("api/home-comment/delete-comment?comment_id=2", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {"message": "Comment deleted successfully"}

def test_delete_home_comment_not_found():
    response = client.delete("api/home-comment/delete-comment?comment_id=3", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}

def test_create_home_subcomment():
    response = client.post("/api/home-comment/create-subcomment?", json={
        "reply_of": 1,
        "posted_by": "66011192",
        "reply_data": "<p>u are gay</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "reply_of": 1,
        "reply_data": "<p>u are gay</p>",
        "create_at": "2021-09-01 12:00:10",
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def create_home_sub_comment():
    response = client.post("/api/home-comment/create-subcomment", json={
        "reply_of": 1,
        "posted_by": "66011192",
        "reply_data": "<p>this is another reply comment</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})

def test_create_home_subcomment_not_found():
    response = client.post("/api/home-comment/create-subcomment?", json={
        "reply_of": 3,
        "posted_by": "66011192",
        "reply_data": "<p>this is another reply comment</p>",
        "create_at": "2021-09-01 12:00:10"
    }, headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}

def test_update_home_subcomment():
    response = client.put("api/home-comment/update-subcomment?subcomment_id=1", json={
        "reply_data": "<p>Update subcomment</p>",
        "create_at": "2021-09-01 12:00:12"
    }, headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "reply_of": 1,
        "reply_data": "<p>Update subcomment</p>",
        "create_at": "2021-09-01 12:00:12",
        "author": {
            "student_id": "66011192",
            "name": "Rachata",
            "surname": "Phondi",
            "year": 2,
            "is_ta": None,
            "ta_course_id": None
        }
    }

def test_update_home_subcomment_not_found():
    response = client.put("api/home-comment/update-subcomment?subcomment_id=3", json={
        "reply_data": "<p>Update subcomment</p>",
        "create_at": "2021-09-01 12:00:12"
    }, headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Subcomment not found"}

def test_delete_home_subcomment():
    response = client.delete("api/home-comment/delete-subcomment?subcomment_id=1", headers={"x-token": get_token()})
    assert response.status_code == 200
    assert response.json() == {"successful": "Subcomment deleted successfully"}

def test_delete_home_subcomment_not_found():
    response = client.delete("api/home-comment/delete-subcomment?subcomment_id=3", headers={"x-token": get_token()})
    assert response.status_code == 404
    assert response.json() == {"detail": "Subcomment not found"}
# SEThreads-API

SEThreads-API is the server-side implementation of SEThreads, a web application designed for Software Engineering students at KMITL. This backend handles API endpoints, database management, and business logic to support thread-based discussions, file uploads, and user interactions.

## Features

- **User Authentication**: Secure user login and registration.
- **Thread Management**: Create, read, update, and delete (CRUD) operations for threads.
- **Engagement System**: Users can likes and comments on threads to interact with peers.
- **File Attachments**: Support for attaching files (e.g., documents, images) to threads.
- **Database Integration**: Efficient data management with SQLite and SQLAlchemy.

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - A modern web framework for building APIs with Python.
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Database interaction and modeling.
- **Database**: SQLite - A lightweight, file-based database.
- **Language**: Python 3.10+
- **Others**:
  - [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation.
  - [Uvicorn](https://www.uvicorn.org/) for running the FastAPI app.

## Installation and Setup

### Prerequisites
- Python 3.10 or higher installed on your system.

### Steps to Set Up Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/skibidi-rizz-SE15/sethreads-api.git
   cd sethreads-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```
   **Acivate a virtual enviroment**:

   Linux
   ```bash
   source .venv/bin/activate
   ```
   Windows
   ```powershell
   .venv\Scripts\activate
   ```
   

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the server**:
   Start the FastAPI application:
   ```bash
   fastapi dev src/main.py
   ```

## Project Structure

```plaintext
sethreads-api/
│
├── src/                             # Main source code for the application
│   ├── __init__.py                  # Marks the directory as a Python package
│   ├── api/                         # API layer for handling HTTP requests and responses
│   │   ├── __init__.py              # Initializes the `api` module
│   │   ├── routers/                 # Contains FastAPI routers for different resources
│   │   │   ├── __init__.py          # Initializes the `routers` module
│   │   │   ├── student.py           # Router for student-related endpoints
│   │   │   ├── thread.py            # Router for thread-related endpoints
│   │   │   ├── comment.py           # Router for comment-related endpoints
│   │   │   ├── home.py              # Router for home-related threads
│   │   │   ├── home_comment.py      # Router for comments on home threads
│   │   ├── api.py                   # Main API entry point that connects all routers
│   │   ├── auth.py                  # Authentication logic and token handling
│   ├── crud/                        # CRUD (Create, Read, Update, Delete) operations
│   │   ├── __init__.py              # Initializes the `crud` module
│   │   ├── student_helper.py        # CRUD helpers for student operations
│   │   ├── thread_helper.py         # CRUD helpers for thread operations
│   │   ├── comment_helper.py        # CRUD helpers for comment operations
│   │   ├── home_helper.py           # CRUD helpers for home threads
│   │   ├── home_comment_helper.py   # CRUD helpers for comments on home threads
│   ├── schemas/                     # Pydantic schemas for request/response validation
│   │   ├── __init__.py              # Initializes the `schemas` module
│   │   ├── comments.py              # Schema definitions for comments
│   │   ├── courses.py               # Schema definitions for courses
│   │   ├── home_comments.py         # Schema definitions for comments on home threads
│   │   ├── home_subcomments.py      # Schema definitions for nested comments on home threads
│   │   ├── home_threads.py          # Schema definitions for home threads
│   │   ├── students.py              # Schema definitions for student objects
│   │   ├── subcomments.py           # Schema definitions for nested comments
│   │   ├── threads.py               # Schema definitions for threads
│   ├── tests/                       # Test suite for the application
│   │   ├── __init__.py              # Initializes the `tests` module
│   │   ├── test_app.py              # Test cases for the core application
│   ├── app.py                       # Entry point for the FastAPI application
│   ├── common.py                    # Common utilities and shared logic
│   ├── database.py                  # Database connection and ORM setup
│   ├── dependencies.py              # Shared dependencies for routes (e.g., authentication)
│   ├── models.py                    # SQLAlchemy models defining database tables
│   └── seed.json                    # Initial seed data for populating the database
│
├── alembic/                         # Database migrations directory
│   ├── versions/                    # Versioned migration scripts
│   ├── README                       # Alembic tool documentation
│   ├── env.py                       # Alembic configuration for database migrations
│   ├── script.py.mako               # Template for creating new migration scripts
├── .gitignore                       # Git ignored files (e.g., virtual environment, logs)
├── README.md                        # Project documentation
├── alembic.ini                      # Alembic configuration file
└── requirements.txt                 # Python dependencies for the project
```

## API Endpoints

Explore and test the API endpoints via the FastAPI Swagger UI at `/docs`. Key endpoints include:

### User Authentication
- `POST /sign-up`: Register a new user.
- `POST /sign-in`: Log in and receive a token.

### Students
- `GET /api/student/get-info?student_id={id}`: Get information about student by there `id`
- `POST /api/student/register-course`: Register student in the course
- `DELETE /api/student/withdraw-course`: Withdraw student's course

### Threads
- `GET /api/thread/get-all`: Get all threads.
- `GET /api/thread/get-thread?thread_id={t_id}&course_id={c_id}`: Get thread information by `t_id` and `c_id`
- `POST /api/thread/create-thread`: Create a new thread.
- `PUT /api/thread/update-thread`: Update thread information
- `DELETE /api/thread/delete-thread?thread_id={id}`: Delete thread by its `id`

### Comments
- `GET /api/comment/get-comments?thread_id={id}`: Get comments for thread by its `id`
- `PUT /api/comment/update-comment?comment_id={id}`: Update comment by its `id`
- `POST /api/comment/create-comment`: Create a new comment
- `DELETE /api/comment/delete-comment?comment_id={id}`: Delete comment by its `id`

## Future Enhancements
- **Search Functionality**: Allow users to search threads by title or tags.
- **AI Enhancements**: Integrate AI-powered features to enhance user experience and improve the platform's functionality

## Contributing

Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature or fix description"
   ```
4. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions or suggestions, feel free to reach out:
- **GitHub**: [@serayutaka](https://github.com/serayutaka)
- **GitHub**: [@whatdislol](https://github.com/whatdislol)
- **GitHub**: [@WDTX1402](https://github.com/WDTX1402)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_SQLite_DATABASE_URL = os.getenv("DATABASE_SQLite_URL")
SQLALCHEMY_Postgresql_DATABASE_URL = os.getenv("DATABASE_POSTGRESQL_URL")

try:
    engine = create_engine(
        SQLALCHEMY_Postgresql_DATABASE_URL,
        echo=True  # Set to False in production
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Database connection error: {e}")
    raise

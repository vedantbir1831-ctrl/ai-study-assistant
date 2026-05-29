from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy import Column, Integer, String

DATABASE_URL = "sqlite:///study_assistant.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    summary = Column(String)
    quiz = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, nullable=True)

Base.metadata.create_all(bind=engine)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
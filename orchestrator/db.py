from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://user:password@postgres/jobs"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String, primary_key=True)
    state = Column(String)
    attempt = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    error = Column(Text, nullable=True)
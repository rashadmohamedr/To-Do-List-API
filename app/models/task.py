from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

# Task table
class Task(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String,nullable=True)
    completed = Column(Boolean, default=False)
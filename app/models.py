from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Note(Base):
    __tablename__ = "notes"


    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
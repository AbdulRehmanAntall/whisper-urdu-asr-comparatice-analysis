from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Recording(Base):
    __tablename__ = "recordings"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    prompt_id = Column(Integer, ForeignKey("urdu_text.id"), nullable=False)  # FK to urdu_text
    filename = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UrduText(Base):
    __tablename__ = "urdu_text"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

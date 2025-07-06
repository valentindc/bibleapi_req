from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Verse(Base):
    __tablename__ = "verses"
    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, index=True)
    text = Column(Text)           # JSON raw text de bible-api.com
    count = Column(Integer, default=0)

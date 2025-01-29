from sqlalchemy import Column, Integer, String, Text
from .database import Base

class TarotCard(Base):
    __tablename__ = "tarot_cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    image_url = Column(String(255))
    meaning_upright = Column(Text)
    meaning_reversed = Column(Text)

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    dob = Column(String(10))
    gender = Column(String(50))
    question = Column(Text)

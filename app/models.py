from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}  # <-- ADD THIS

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)



class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), unique=True, index=True)
    price = Column(Float)
    volume = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

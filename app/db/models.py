from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(50))

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), unique=True, index=True)
    price = Column(Float)
    volume = Column(BigInteger)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, Float, String, DateTime

class Tweet(Base):
    __tablename__ = 'tweets'
    
    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    text = Column(String(500), nullable=False)
    def __init__(self, latitude: float, longitude: float, created_at: datetime, text: str):
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = created_at
        self.text = text

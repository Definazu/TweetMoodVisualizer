# database.py
"""
Database module for SQLAlchemy configuration and operations.

Contains database engine setup, session management, and table creation logic.
"""

from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()
db_path = os.path.join(os.path.dirname(__file__), 'DataTweets.db')
engine = create_engine(f'sqlite:///{db_path}', connect_args={'check_same_thread': False})
Session = scoped_session(sessionmaker(bind=engine))

def init_db():
    """Initialize database schema.
    
    Creates all defined tables if they don't exist.
    Should be called once at application startup.
    """
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")

def table_exists(table_name: str) -> bool:
    """Check if specified table exists in database.
    
    Args:
        table_name (str): Name of the table to check
        
    Returns:
        bool: True if table exists, False otherwise
    """
    return inspect(engine).has_table(table_name)

def create_table(table_name: str):
    """Create dynamic ORM model for specified table name.
    
    Args:
        table_name (str): Name for the new table
        
    Returns:
        DeclarativeMeta: SQLAlchemy model class with:
        - id (primary key)
        - latitude (float)
        - longitude (float)
        - created_at (datetime)
        - text (varchar 500)
    """
    class Tweet(Base):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}
        
        id = Column(Integer, primary_key=True)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        created_at = Column(DateTime, nullable=False)
        text = Column(String(500), nullable=False)

    if not table_exists(table_name):
        Base.metadata.create_all(bind=engine, tables=[Tweet.__table__])
    
    return Tweet
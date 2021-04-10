'''
Database tables Classes are defined here
'''
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# database table
class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

# database table
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    location = Column(String, index=True)
    date = Column(String, index=True)
    isLost = Column(Integer, default = 1)
    isFound = Column(Integer, default = 0)
    owner_id = Column(String, ForeignKey("users.email"))

    owner = relationship("User", back_populates="items")
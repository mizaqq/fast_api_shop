from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Float, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float,index=True)
    tax = Column(Float,index=True)
    is_active = Column(Boolean, default=True)

class Cart(Base):
    __tablename__="carts"
    
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    item_id =Column(Integer, ForeignKey("items.id"))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    products = relationship("Item")
    owner = relationship("User")

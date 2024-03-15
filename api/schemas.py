from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: float = 0
    tax: float | None = None
    
class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
        
class CartBase(BaseModel):
    id: int
    
class CartCreate(CartBase):
    pass 

class Cart(CartBase):
    items: list[Item]= []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
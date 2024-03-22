from pydantic import BaseModel
from datetime import datetime
from typing import List

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
    pass

class Cart(CartBase):
    id: int
#    created_at: datetime
    user: int
    items: List[Item]

    class Config:
        orm_mode = True
class CartCreate(Cart):
    pass

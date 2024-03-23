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
    username: str
    email: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str


        
class CartBase(BaseModel):
    pass

class Cart(CartBase):
    id: int
    user: int
    items: List[Item]

    class Config:
        orm_mode = True
class CartCreate(Cart):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
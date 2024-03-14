from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: float = 0
    tax: float | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Foo",
                    "Desc": "Nice Item",
                    "price": 35.4,
                    "tax": 0,
                }
            ]
        }
    } 
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
    cart: list[Item] = []

    class Config:
        orm_mode = True
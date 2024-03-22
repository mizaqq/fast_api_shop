from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.sql import func
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#TODO HASH PASSWORD
#TODO USER AUTH
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#TODO deactivate item

def create_cart(db: Session,cart_create: schemas.Cart):
    items=[]
    for i in cart_create.items:
        items.append(db.query(models.Item).filter(models.Item.id == i.id).first())
    db_cart = models.Cart()
    for i in items:
        if i is None:
            raise HTTPException(status_code=404, detail="One of items not found")
        if i.is_active==False:
            raise HTTPException(status_code=404, detail="One of items inactive")
        db_cart.items.append(i)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_cart(db: Session, cart_id: int):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if cart:
        cart.items
    return cart

def delete_item_from_cart(db:Session, cart_id:int, item_id:int):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if cart:
        item=db.query(models.Item).filter(models.Item.id==item_id).first()
        if item==None or item not in cart.items:
            raise HTTPException(status_code=404, detail="Item not found")
        cart.items.remove(item)
        cart.updated_at=func.current_timestamp()
        db.commit()
        db.refresh(cart)
    if cart:
        cart.items
    return cart
    
def add_item_to_cart(db,cart_id,items):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if cart:
        items_db=[]
        for i in items:
            items_db.append(db.query(models.Item).filter(models.Item.id == i.id).first())
        for i in items_db:
            if i is None:
                raise HTTPException(status_code=404, detail="One of items not found")
            if i.is_active==False:
                raise HTTPException(status_code=404, detail="One of items inactive")
            if i in cart.items:
                raise HTTPException(status_code=404, detail="This item is already in the cart!")
            cart.items.append(i)
        cart.updated_at=func.current_timestamp()
        db.commit()
        db.refresh(cart)
    if cart:
        cart.items    
    return cart
        

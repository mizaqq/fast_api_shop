from sqlalchemy.orm import Session
from typing import Optional,Annotated
from . import models, schemas
from fastapi import HTTPException, status
from sqlalchemy.sql import func
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


##temp
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    if current_user.is_active==False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_access_token(
    db:Session, form_data
) -> schemas.Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


def read_users_me(
    db: Session,
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return current_user



def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#TODO HASH PASSWORD
#TODO USER AUTH

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username = user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
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
        


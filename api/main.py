from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Optional,Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext


app = FastAPI()

from api import models, crud, schemas,database
from api.database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#TODO ADD TOKEN AUTH

        
@app.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends(),],db: Session = Depends(database.get_db)
) -> schemas.Token:
    return crud.get_access_token(db,form_data)


@app.post("/users/",response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
    
@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(crud.get_current_active_user)]
):
    return current_user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@app.post("/items/", response_model=schemas.Item)
def create_item(
   item: schemas.ItemCreate, db: Session = Depends(database.get_db)
):
    return crud.create_item(db=db, item=item)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

#TODO deactivate item

@app.post("/items/carts")
def create_cart(
    cart_create: schemas.CartCreate, db: Session = Depends(database.get_db)
):
    return crud.create_cart(db=db,cart_create=cart_create)

@app.get("/items/cart/{cart_id}")
def read_cart(cart_id: int, db: Session = Depends(database.get_db)):
    return crud.get_cart(db=db, cart_id=cart_id)

@app.delete("/items/cart/{cart_id}/{item_id}")
def update_cart_delete(cart_id: int, item_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_item_from_cart(db=db,cart_id=cart_id,item_id=item_id)

@app.put("/items/cart/{cart_id}")
def update_cart_add(cart_id: int,items: list[schemas.Item], db: Session = Depends(database.get_db)):
    return crud.add_item_to_cart(db=db,cart_id=cart_id,items=items)
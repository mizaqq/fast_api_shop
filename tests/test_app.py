from fastapi.testclient import TestClient
from api.main import app, get_db


from api import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from api.database import SessionLocal, engine


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_create_user():
    response = client.post("/users/",
        headers={
        'accept': 'application/json',
        'Content-Type': 'application/json',
        },
        json={"email": "test@test.com",  "password": "test"}
    )
    assert response.status_code == 200
    assert response.json() == {  "email": "test@test.com","id":1, "is_active": True}
 
    
def test_create_user_already_registered():
    response = client.post("/users/",
        headers={
        'accept': 'application/json',
        'Content-Type': 'application/json',
        },
        json={"email": "test@test.com",  "password": "test"}
    )
    assert response.status_code == 400
    assert response.json() =={"detail": "Email already registered"}


def test_get_users():
    header = {
        'accept': 'application/json'
    }
    response = client.get("/users/",headers=header)
    assert response.status_code == 200
    
def test_read_user():
    header = {
        'accept': 'application/json'
    }
    response = client.get("/users/1",headers=header)
    assert response.status_code == 200
    assert response.json() == {  "email": "test@test.com","id":1, "is_active": True}
    
def test_create_item():
    header = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
        }
    response = client.post("/items/", headers = header, json = {
            "title": "string",
            "description": "string",
            "price": 0,
            "tax": 0
              })
    assert response.status_code == 200
    assert response.json() == {
          "title": "string",
          "description": "string",
          "price": 0,
          "tax": 0,
          "id": 1,
          "is_active": True
        }
def test_read_items():
    header = {
        'accept': 'application/json'
    }
    response = client.get("/items/",headers=header)
    assert response.status_code == 200
    assert response.json() == [
      {
        "title": "string",
        "description": "string",
        "price": 0,
        "tax": 0,
        "id": 1,
        "is_active": True
      }
    ]

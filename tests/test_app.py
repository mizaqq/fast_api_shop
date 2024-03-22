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
    data = response.json()
    data.pop('id', None)
    assert data == {  "email": "test@test.com", "is_active": True}
 
    
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


def test_get_user():
    header = {
        'accept': 'application/json'
    }
    response = client.get("/users/",headers=header)
    assert response.status_code == 200
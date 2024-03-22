from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

'''
def test_create_user():
    response = client.post("/users/",
        json={"email": "string",  "password": "string"}
    )
    assert response.status_code == 200
    assert response.json() =={"email": "string",  "password": "string"}
'''

def test_get_user():
    header = {
        'accept': 'application/json'
    }
    response = client.get("/users/",headers=header)
    assert response.status_code == 200
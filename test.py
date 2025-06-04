from fastapi import FastAPI, HTTPException, Query
from fastapi.testclient import TestClient
app = FastAPI()
from api import app # Assuming the functions are in api.py
client = TestClient(app)
client.get("/")  # This line is just to ensure the app is initialized
# Test cases
def test_greet():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
def test_read_item():
    response = client.get("/items/1?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "query": "test"}
def test_read_item_invalid_id():
    response = client.get("/items/-1?q=test")
    assert response.status_code == 400
    assert response.json() == {"detail": "Item ID must be a positive integer"}
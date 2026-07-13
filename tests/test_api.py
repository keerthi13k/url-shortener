from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

with patch('app.database.create_engine'), \
     patch('app.database.SessionLocal'), \
     patch('app.cache.redis.Redis'):
    from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "URL Shortener" in response.json()["message"]

def test_health():
    response = client.get("/")
    assert response.status_code == 200

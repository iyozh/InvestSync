from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

def test_get_intraday_prices():
   pass

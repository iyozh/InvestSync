import json
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

@patch("app.src.services.redis_service.RedisService.get_cached_value")
@patch("httpx.get")
def test_get_quote(mock_httpx_get, mock_get_cached_value):
    with open(f"{Path().absolute()}/test_data/quote.json") as fp:
        mocked_quote_response = json.loads(fp.read())

    mock_get_cached_value.return_value = mocked_quote_response
    mock_httpx_get.return_value.json.return_value = mocked_quote_response

    response = client.get("/tickers/quote/META")

    assert response.status_code == 200
    assert response.json() == mocked_quote_response

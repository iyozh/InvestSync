from unittest.mock import patch
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

@patch("app.src.services.redis_service.RedisService.get_cached_value")
@patch("httpx.get")
def test_get_stock_info(mock_httpx_get, mock_get_cached_value):
        mocked_response = [{"symbol": "META",
                                  "change": -0.74,
                                  "changePercent": -0.00317,
                                  "currency": "USD",
                                  "peRatio": 28.92,
                                  "iexRealtimePrice": None,
                                  "latestPrice": 232.78}]
        mock_get_cached_value.return_value = mocked_response
        mock_httpx_get.return_value.json.return_value = mocked_response

        response = client.get("/tickers/quote/AAPL")

        assert response.status_code == 200
        assert response.json() == mocked_response

import json
from pathlib import Path

from fastapi.testclient import TestClient
from app.src.main import app


def test_get_ticker_history():
   with TestClient(app) as client:
      with open(f"{Path().absolute()}/test_data/history.json") as fp:
         ticker_history = json.loads(fp.read())

      ticker_symbol = ticker_history.get('symbol')
      history = ticker_history.get('history')

      response = client.get(f'/tickers/history/{ticker_symbol}')

      assert response.status_code == 200
      for history_snapshot in history:
         assert history_snapshot in response.json()

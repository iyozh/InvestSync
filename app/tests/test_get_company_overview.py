import json
from pathlib import Path

from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

def test_get_tickers_overview():
   response = client.get("/tickers/")

   with open(f"{Path().absolute()}/test_data/tickers_overview.json") as fp:
      ticker_overviews = json.loads(fp.read())

   assert response.status_code == 200
   for overview in ticker_overviews:
      assert overview in response.json()


def test_single_company_overview():
   ticker_symbol = 'META'
   response = client.get(f"/tickers/{ticker_symbol}")

   with open(f"{Path().absolute()}/test_data/tickers_overview.json") as fp:
      ticker_overviews = json.loads(fp.read())

   filtered_overviews = list(
      filter(lambda overview: overview.get('symbol') == ticker_symbol,ticker_overviews)
   )

   overview = None
   if filtered_overviews:
      overview = filtered_overviews[0]

   assert response.status_code == 200
   assert response.json() == overview


def test_get_overview_of_non_existing_ticker():
   with TestClient(app) as client:
      response = client.get("/tickers/GOOD")

      assert response.status_code == 400

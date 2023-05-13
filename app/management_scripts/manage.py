import json
from pathlib import Path

import requests
import typer
from app.src.core.config import settings
from app.src.core.constants import INITIAL_TICKERS, COMPANY_OVERVIEW_API_URL, HISTORY_PRICES_API_URL
from app.src.db.session import SessionLocal
from app.src.main import logger
from app.src.models.ticker import Ticker
from app.src.models.ticker_history import TickerHistory
from app.src.models.ticker_overview import TickerOverview

cli = typer.Typer()

@cli.command()
def populate_db():
    db = SessionLocal()

    for symbol in INITIAL_TICKERS:
        ticker = Ticker(symbol=symbol)
        db.add(ticker)
    db.commit()

    logger.info("Getting companies overview data ...")

    for ticker in db.query(Ticker):

        logger.info(f"Getting {ticker.symbol} company overview data ...")

        api_url = COMPANY_OVERVIEW_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
        response = requests.get(api_url)
        company_overview_snapshot = response.json()

        logger.info(f"Received {ticker.symbol} company overview data")

        if company_overview_snapshot:
            company_overview = company_overview_snapshot[0]
            ticker_overview = TickerOverview(
                ticker_id=ticker.id,
                name=company_overview.get('companyName'),
                description=company_overview.get('longDescription'),
                country=company_overview.get('country'),
                sector=company_overview.get('sector'),
                industry=company_overview.get('industry')
            )
            db.add(ticker_overview)

        db.commit()

    logger.info(f"Companies data added to DB")

    ticker_history_prices = []

    logger.info(f"Getting historical prices for tickers ...")
    for ticker in db.query(Ticker):

        logger.info(f"Getting {ticker.symbol} historical prices ...")

        api_url = HISTORY_PRICES_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
        response = requests.get(api_url)
        ticker_history = response.json()

        logger.info(f"Received {ticker.symbol} historical prices")

        if ticker_history:
            for fact in ticker_history:
                ticker_history_price = TickerHistory(ticker_id=ticker.id,
                                                     date=fact.get('priceDate'),
                                                     open=fact.get('open'),
                                                     close=fact.get('close'),
                                                     volume=fact.get('volume'),
                                                     low=fact.get('low'),
                                                     high=fact.get('high'))
                ticker_history_prices.append(ticker_history_price)

    db.bulk_save_objects(ticker_history_prices)
    db.commit()

    logger.info("Historical prices added to DB")

    db.close()

@cli.command()
def populate_test_db():
    db = SessionLocal()

    with open(f"{Path().absolute().parent}/test_data/tickers_overview.json") as fp:
        ticker_overviews = json.loads(fp.read())

    for overview in ticker_overviews:
        db.add(Ticker(symbol=overview.get('symbol')))

    db.commit()

    for ticker in db.query(Ticker):
        filtered_overviews = list(
            filter(lambda overview: overview.get('symbol') == ticker.symbol, ticker_overviews)
        )

        overview = None
        if filtered_overviews:
            overview = filtered_overviews[0]

        overview = overview.get('overview')
        db.add(
            TickerOverview(
                ticker_id=ticker.id,
                **overview
            )
        )

    db.commit()

    with open(f"{Path().absolute().parent}/test_data/history.json") as fp:
        ticker_history = json.loads(fp.read())

    ticker_symbol = ticker_history.get('symbol')
    history = ticker_history.get('history')

    ticker = db.query(Ticker).filter(Ticker.symbol == ticker_symbol).first()

    for snapshot in history:
        db.add(
            TickerHistory(
                ticker_id=ticker.id,
                **snapshot
            )
        )

    db.commit()
    db.close()


if __name__ == "__main__":
    cli()

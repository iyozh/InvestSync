import requests
import typer

from app.src.core.config import settings
from app.src.core.constants import INITIAL_TICKERS, COMPANY_OVERVIEW_API_URL
from app.src.db.session import SessionLocal
from app.src.models.ticker import Ticker
from app.src.models.ticker_overview import TickerOverview


def populate_db():
    db = SessionLocal()

    for symbol in INITIAL_TICKERS:
        ticker = Ticker(symbol=symbol)
        db.add(ticker)
    db.commit()

    for ticker in db.query(Ticker):

        api_url = COMPANY_OVERVIEW_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
        response = requests.get(api_url)
        company_overview_snapshot = response.json()

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
    db.close()


if __name__ == "__main__":
    typer.run(populate_db)

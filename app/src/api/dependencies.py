from typing import Generator

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.src.db.session import SessionLocal
from app.src.repos.ticker_repo import TickerRepo


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_ticker_or_raise_404(symbol: str, db: Session = Depends(get_db)):
    ticker_repo = TickerRepo()
    ticker = ticker_repo.get_by_symbol(db, symbol)

    if not ticker:
        raise HTTPException(
            status_code=400, detail="Ticker doesn't exist"
        )

    return ticker

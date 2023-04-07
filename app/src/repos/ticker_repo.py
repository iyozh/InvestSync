from typing import Optional, Type

from sqlalchemy.orm import Session

from app.src.models.ticker import Ticker
from app.src.repos.base_repo import BaseRepo, ModelType


class TickerRepo(BaseRepo):
    def __init__(self, model: Type[Ticker] = Ticker):
        """
        Repo for work with ticker table
        """
        super().__init__(model)

    def get_by_symbol(self, db: Session, symbol: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.symbol == symbol).first()

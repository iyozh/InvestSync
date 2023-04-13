from typing import Type
from sqlalchemy import func, desc, tuple_
from sqlalchemy.orm import Session

from app.src.models.ticker import Ticker
from app.src.models.ticker_history import TickerHistory
from app.src.repos.base_repo import BaseRepo


class TickerHistoryRepo(BaseRepo):
    def __init__(self, model: Type[TickerHistory] = TickerHistory):
        """
        Repo for work with ticker_history table
        """
        super().__init__(model)

    def get_top_tickers_by_percentage_change(self, db: Session, limit: int, offset: int):
        row_number_column = func.row_number().over(partition_by=self.model.ticker_id,
                                                   order_by=desc(self.model.date)).label('row_number')

        subquery = db.query(self.model.ticker_id, self.model.date, row_number_column).subquery()
        last_7_rows_subquery = db.query(subquery.c.ticker_id, subquery.c.date).filter(subquery.c.row_number <= 7).subquery()
        qeury = db.query(self.model.id,
                         ).filter(tuple_(self.model.ticker_id, self.model.date).in_(last_7_rows_subquery)).subquery()
        query = db.query(self.model.ticker_id, func.count(
            (func.max(self.model.close) - func.min(self.model.close) / func.min(self.model.close * 100))).label('change_percentage')).filter(self.model.id.in_(qeury)).group_by(
            self.model.ticker_id).order_by('change_percentage')

        return "Hi!"
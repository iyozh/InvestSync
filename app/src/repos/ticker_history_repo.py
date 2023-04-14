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

        subquery = db.query(self.model, row_number_column).subquery()
        last_7_rows_subquery = db.query(subquery).filter(subquery.c.row_number <= 7).subquery()
        statistics_query = db.query(last_7_rows_subquery.c.ticker_id,
                         ((func.max(last_7_rows_subquery.c.close) - func.min(last_7_rows_subquery.c.close))
                          / (func.min(last_7_rows_subquery.c.close)) * 100).label('change_percentage')).group_by(
            last_7_rows_subquery.c.ticker_id).order_by(desc('change_percentage')).limit(4).subquery()
        query = db.query(self.model).join(statistics_query, statistics_query.c.ticker_id == self.model.id).all()
        return "Hi!"
from app.src.models.ticker import Ticker
from sqladmin import ModelView

class TickerAdmin(ModelView, model=Ticker):
    column_list = [Ticker.id, Ticker.symbol]

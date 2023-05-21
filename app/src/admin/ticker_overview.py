from sqladmin import ModelView

from app.src.models.ticker_overview import TickerOverview

ticker_overview_columns = [
        TickerOverview.ticker_id,
        TickerOverview.name,
        TickerOverview.industry,
        TickerOverview.country,
        TickerOverview.sector,
        TickerOverview.description,
    ]

class TickerOverviewAdmin(ModelView, model=TickerOverview):
    column_list = ticker_overview_columns
    column_searchable_list = ticker_overview_columns
    column_formatters = {TickerOverview.description: lambda model, a: model.description[:30] + '...'}

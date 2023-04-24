DEFAULT_FIELD_PLACEHOLDER = '—'

INITIAL_TICKERS = ['AAPL', 'TSLA', 'MSFT', 'META','AMZN']

COMPANY_OVERVIEW_API_URL = 'https://api.iex.cloud/v1/data/core/company/{symbol}?token={api_key}'

HISTORY_PRICES_API_URL = 'https://api.iex.cloud/v1/data/CORE/HISTORICAL_PRICES/{symbol}?' \
                         'token={api_key}&range=1y&&filter=open,low,high,close,volume,priceDate'

HISTORY_PRICES_UPDATE_API_URL = 'https://api.iex.cloud/v1/data/CORE/HISTORICAL_PRICES/{symbol}?' \
                         'token={api_key}&from={date}&filter=open,low,high,close,volume,priceDate'

INTRADAY_PRICES_API_URL = 'https://api.iex.cloud/v1/data/CORE/INTRADAY_PRICES/{symbol}?range=1d&token={api_key}' \
                          '&sort=desc&filter=open,low,high,close,volume,priceDate,minute'

QUOTE_API_URL = 'https://api.iex.cloud/v1/data/CORE/QUOTE/{symbol}?token={api_key}&' \
                'filter=symbol,change,changePercent,currency,peRatio,iexRealtimePrice,latestPrice'

TOP_TICKERS_AMOUNT = 4

QUOTE_EXPIRATION_TIME = 60 # in seconds
INTRADAY_PRICES_EXPIRATION_TIME = 60 # in seconds
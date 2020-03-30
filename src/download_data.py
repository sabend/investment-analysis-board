"""
Download stock quotes from finance.yahoo API
"""
import datetime as dt
import plotly.graph_objects as go
import plotly.offline as plt
from src.data.YahooDataLoader import YahooDataLoader
from src.data.IngDataScraper import IngDataScraper
from src.finance.components.StockMarketIndex import StockMarketIndex


# download quotes from Yahoo finance
dl = YahooDataLoader()

data = dl.fetch(
    ticker='%5EGDAXI',
    start=dt.datetime(2005, 1, 1),
    end=dt.datetime(2020, 3, 26),
    freq='1wk'
)

fig = go.Figure(
    data=go.Scatter(x=data['Date'], y=data['Close']),
    layout={'yaxis': {'tickformat': ','}}
)
plt.plot(fig)


# download stock index components
ing_scraper = IngDataScraper()

components = ing_scraper.get_components('DE0008469008')
print(*list(components.keys()), sep='\n')


# get market capitalisation for stock
ing_scraper.get_market_cap('DE0005200000')


# download key financials
pnl, balance = ing_scraper.get_financials_for_stock('DE000A1EWWW0')
print(pnl)
print(balance)


# build index
dax = StockMarketIndex(
    isin='DE0008469008',
    yahoo_ticker='%5EGDAXI'
)




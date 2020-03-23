"""
Download stock quotes from finance.yahoo API
"""
import datetime as dt
import plotly.graph_objects as go
import plotly.offline as plt
from src.data.YahooDataLoader import YahooDataLoader

dl = YahooDataLoader()

data = dl.fetch(
    ticker='%5EGDAXI',
    start=dt.datetime(2005, 1, 1),
    end=dt.datetime(2020, 3, 16),
    freq='1wk'
)

fig = go.Figure(
    data=go.Scatter(x=data['Date'], y=data['Close']),
    layout={'yaxis': {'tickformat': ','}}
)
plt.plot(fig)














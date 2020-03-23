"""
Application for visualisation
"""
import datetime as dt
from dateutil.relativedelta import relativedelta
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from src.data.YahooDataLoader import YahooDataLoader

# data setup
default_index_tickers = [
    '%5EGDAXI',     # DAX
    '%5EMDAXI',     # MDAX
    '%5ESDAXI',     # SDAX
    '%5EDJI',       # DOW JONES
    '%5EGSPC',      # S&P 500
    '%5ESTOXX50E',  # Eurostoxx 50
    '%5EN225',      # Nikkei 225
]

default_commodity_tickers = [
    'GC%3DF',       # gold
]

# global parameters
date_format_display = 'DD.MM.YYYY'
date_format_internal = '%Y-%m-%d'

margin_style = {'l': 50, 'r': 50, 't': 80, 'b': 20}

# initialise arguments
init_start_date = dt.date.today() - relativedelta(years=1)
init_end_date = dt.date.today()-dt.timedelta(days=1)

# app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = html.Div(
    [
        dbc.Row(
            id='pane',
            children=[
                # control sidebar
                dbc.Col(
                    id='sidebar',
                    sm=12,
                    md=3,
                    children=[
                        html.Div(
                            children=[
                                html.H2('Investment Analysis Board'),
                                html.P('Period:'),
                                dcc.DatePickerRange(
                                    id='dpr-date-period',
                                    display_format=date_format_display,
                                    start_date=init_start_date,
                                    end_date=init_end_date
                                ),
                                html.Br(),
                                html.Br(),
                                html.P('Frequency:'),
                                dcc.Dropdown(
                                    id='drp-freq',
                                    options=[
                                        {'label': 'daily', 'value': '1d'},
                                        {'label': 'weekly', 'value': '1wk'},
                                        {'label': 'monthly', 'value': '1mo'}
                                    ],
                                    value='1d',
                                    style={
                                        'width': '12rem'
                                    }
                                ),
                                html.Br(),
                                html.Button(
                                    id='btn-run',
                                    children='Run'
                                ),
                                html.Hr(),
                                html.Span(
                                    [
                                        html.P('Axis type (stock index data):'),
                                        dcc.RadioItems(
                                            id='rd-axis-scaling',
                                            options=[
                                                {'label': 'linear', 'value': 'linear'},
                                                {'label': 'logarithmic', 'value': 'log'}
                                            ],
                                            value='linear',
                                            inputStyle={
                                                'margin-left': '5px',
                                                'margin-right': '5px'
                                            }
                                        )
                                    ]
                                ),
                                html.Hr(),
                                html.P('Stock index tickers:'),
                                dcc.Textarea(
                                    id='txtr-index-tickers',
                                    value='\n'.join(default_index_tickers),
                                    style={
                                        'height': '12rem',
                                        'width': '12rem'
                                    }
                                ),
                                html.P('Commodity tickers:'),
                                dcc.Textarea(
                                    id='txtr-commodity-tickers',
                                    value='\n'.join(default_commodity_tickers),
                                    style={
                                        'height': '12rem',
                                        'width': '12rem'
                                    }
                                )
                            ],
                            style={
                                'padding': '1rem'
                            }
                        )
                    ]
                ),
                # body
                dbc.Col(
                    id='body',
                    sm=12,
                    md=9,
                    children=[
                        dbc.Row(
                            children=[
                                # stock index values
                                dbc.Col(
                                    sm=12,
                                    xl=6,
                                    children=[dcc.Graph(id='grph-index-values')]
                                ),
                                # stock index volume
                                dbc.Col(
                                    sm=12,
                                    xl=6,
                                    children=[dcc.Graph(id='grph-index-volume')]
                                )
                            ]
                        ),
                        dbc.Row(
                            children=[
                                # price-earnings and price-book ratios
                                dbc.Col(
                                    sm=12,
                                    xl=6,
                                    children=[dcc.Graph(id='grph-pe-pb')]
                                ),
                                # commodity prices
                                dbc.Col(
                                    sm=12,
                                    xl=6,
                                    children=[dcc.Graph(id='grph-commodity-prices')]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('grph-index-values', 'figure'),
        Output('grph-index-volume', 'figure'),
        Output('grph-commodity-prices', 'figure')
    ],
    [
        Input('btn-run', 'n_clicks')
    ],
    [
        State('dpr-date-period', 'start_date'),
        State('dpr-date-period', 'end_date'),
        State('drp-freq', 'value'),
        State('txtr-index-tickers', 'value'),
        State('txtr-commodity-tickers', 'value'),
        State('rd-axis-scaling', 'value')
    ]
)
def render_plots(n_clicks, start_date, end_date, freq, index_tickers, commodity_tickers, yaxis_scaling):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        if (start_date is None) or (end_date is None) or (not index_tickers and not commodity_tickers):
            raise dash.exceptions.PreventUpdate

        index_ticker_list = index_tickers.split('\n')
        commodity_ticker_list = commodity_tickers.split('\n')
        value_traces = list()
        volume_traces = list()
        commodity_traces = list()

        ticker_value_yaxis = {'type': yaxis_scaling}
        if yaxis_scaling == 'linear':
            ticker_value_yaxis['tickformat'] = ','

        start = dt.datetime.strptime(start_date.split('T')[0], date_format_internal)
        end = dt.datetime.strptime(end_date.split('T')[0], date_format_internal)

        dl = YahooDataLoader()

        for ticker in index_ticker_list:
            if not ticker:
                continue

            ticker_data = dl.fetch(
                ticker=ticker,
                start=start,
                end=end,
                freq=freq
            )
            value_traces.append({
                'x': ticker_data['Date'],
                'y': ticker_data['Close'],
                'type': 'scatter',
                'name': ticker
            })
            volume_traces.append({
                'x': ticker_data['Date'],
                'y': ticker_data['Volume'],
                'type': 'scatter',
                'name': ticker
            })

        for ticker in commodity_ticker_list:
            if not ticker:
                continue

            ticker_data = dl.fetch(
                ticker=ticker,
                start=start,
                end=end,
                freq=freq
            )
            commodity_traces.append({
                'x': ticker_data['Date'],
                'y': ticker_data['Close'],
                'type': 'scatter',
                'name': ticker
            })

        value_plot = {
            'data': value_traces,
            'layout': {
                'title': 'Index Values',
                'yaxis': ticker_value_yaxis,
                'showlegend': True,
                'margin': margin_style
            }
        }
        volume_plot = {
            'data': volume_traces,
            'layout': {
                'title': 'Index Volume',
                'showlegend': True,
                'margin': margin_style
            }
        }
        commodity_plot = {
            'data': commodity_traces,
            'layout': {
                'title': 'Commodity Prices',
                'showlegend': True,
                'margin': margin_style
            }
        }

        return value_plot, volume_plot, commodity_plot

if __name__ == '__main__':
    app.run_server(
        debug=True,
        port=8888
    )

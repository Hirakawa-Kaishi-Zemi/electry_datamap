import itertools
from datetime import datetime

import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc

drop_down = ['1day', '1month']
if drop_down == '1day':
    df = pd.read_csv("csv/1day_kwh.csv")
else:
    df = pd.read_csv("csv/1month_kwh.csv")

company = [k for k, i in itertools.groupby(df['エリア'])]


def setting():
    sidebar = html.Div([
        dbc.Row(
            [
                html.H5('Settings',
                        style={'margin-top': '10px', 'margin-left': '15px'})

            ], style={"height": "5vh"}, className='bg-light text-white font-italic'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [html.Div([
                        html.P('Select a period of time',
                               style={'margin-top': '8px',
                                      'margin-bottom': '4px'},
                               className='font-weight-bold'),
                        dcc.Dropdown(id='my-cat-picker', multi=False, value='cat0',
                                     options=[{'label': x, 'value': x}
                                              for x in drop_down],
                                     style={'width': '120px'}
                                     ),
                        html.P('Select The companies',
                               style={'margin-top': '16px',
                                      'margin-bottom': '4px'},
                               className='font-weight-bold'),
                        dcc.Dropdown(id='my-corr-picker', multi=True,
                                     value=company,
                                     options=[{'label': x, 'value': x}
                                              for x in company],
                                     style={'width': '320px'}
                                     )

                    ])
                    ]),

                dbc.Col(
                    [html.Div([
                        html.P('Select a start and end date',
                               style={'margin-top': '16px', 'margin-bottom': '4px'}, ),
                        dcc.DatePickerRange(id='my_date_picker',
                                            min_date_allowed=datetime(
                                                2019, 1, 1),
                                            max_date_allowed=datetime.today(),
                                            start_date=datetime(
                                                2022, 1, 1),
                                            end_date=datetime.today()
                                            ),

                        html.P(
                            html.Button(id='my-button', n_clicks=0, children='apply',
                                        style={'margin-top': '16px'},
                                        className='bg-dark text-white'
                                        ),
                        )
                    ]),
                        # className='bg-secondary text-white'

                    ], style={"height": "50vh"}
                )
            ])

    ])
    content = html.Div([dbc.Row(
        [
            dbc.Col(
                [
                    html.P('arrow map'),
                ],
                # className='bg-white'
            ),
            dbc.Col(
                [
                    html.P('heatmap')
                ],
                # className='bg-dark text-white'
            )
        ],
        style={"height": "50vh"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Correlation linegragh')
                    ],
                    # className='bg-light'
                )
            ],
            style={"height": "50vh"}
        )])

    return dbc.Container([
        dbc.Row(
            [
                dbc.Col(sidebar, className='bg-primary')

            ], style={"height": "35vh"}),
        dbc.Row(
            [
                dbc.Col(content, className='bg-dark')
            ]),
    ], fluid=True)

    # html.H1(children='折れ線グラフとかとか表示する')

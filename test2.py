from dash import Dash, html, dcc
import dash
import plotly.express as px
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from japanmap import picture
import itertools

# 電力データ
df1 = pd.read_csv("csv/areamap.csv")

drop_down = ['1day', '1month']
if drop_down == '1day':
    df = pd.read_csv("csv/1day_kwh.csv")
else:
    df = pd.read_csv("csv/1month_kwh.csv")

company = [k for k, i in itertools.groupby(df['エリア'])]


app = dash.Dash(external_stylesheets=[dbc.themes.VAPOR])
# app = Dash(__name__)

app.title = '電力データマップ'
app.layout = html.Div([
    html.H4(children='electric power datemap'),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='dashboard', value='tab-1'),
        dcc.Tab(label='detail', value='tab-2'),
        dcc.Tab(label='electric company', value='tab-3')

    ]),
    html.Div(id='tabs-example-content')

])


@app.callback(Output('tabs-example-content', 'children'), Input('tabs-example', 'value'))
#Output('my_graph', 'figure'),
#   [Input('my_ticker_symbol', 'value'),
# Input('my_date_picker', 'start_date'),
#  Input('my_date_picker', 'end_date')])
def render_content(tab):
    if tab == 'tab-1':
        
        content = html.Div([
            dbc.Row(
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
                       
                    ]
                    # className='bg-dark text-white'
                )
            ],
            style={"height": "50vh"}),
            dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('power linegragh')
                    ],
                    # className='bg-light'
                )
            ],
            style={"height": "50vh"}
              )])
        return setting() ,dbc.Container([
           
             dbc.Row(
               [
                   dbc.Col(content,  className='bg-dark')
            ]), 
                 ], fluid=True)
        

    
        # html.H1(children='折れ線グラフとかとか表示する')

    elif tab == 'tab-2':
        content = html.Div([
            
            dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Power forecast')
                    ],
                    # className='bg-light'
                )
            ],
            style={"height": "50vh"}),
            dbc.Row([
                dbc.Col(
                    [
                        html.P('pie chart'),
                    ],
                    # className='bg-white'
                ),
                dbc.Col(
                    [
                        html.P('power ratio')
                    ],
                    # className='bg-dark text-white'
                )
            ],
            style={"height": "50vh"})
              ])
        return setting() ,dbc.Container([
           
             dbc.Row(
               [
                   dbc.Col(content,  className='bg-dark')
            ]), 
                 ], fluid=True)
             
    elif tab == 'tab-3':
        return html.Div([

            html.H1('３個目のタブの内容表示'),

            html.Div([
                # html.Img(src=app.get_asset_url("colormap.png"),alt='japan',style={'width':'50%','height':'50'}),
                html.Img(src=app.get_asset_url("colormap.png"),
                     alt='japan', style={'display': 'inline-block'}),
                #  html.Div(html.P('北海道電力'),style={'display': 'inline-block', 'height': '50%', 'width': '50%'}),

                html.Div([
                    html.H1('<凡例>'),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#9966CC"}),
                            html.Span(':北海道電力')
                        ], style={'line-height': '100%'}),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#87CEFA"}),
                            html.Span(':東北電力'),
                        ], style={'line-height': '100%'}),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#B0E0E6"}),
                            html.Span(':東京電力'),
                        ], style={'line-height': '100%'}),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#808080"}),
                            html.Span(':北陸電力'),
                        ], style={'line-height': '100%'}),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#98FB98"}),
                            html.Span(':中部電力'),
                        ], style={'line-height': '100%'}),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#9ACD32"}),
                            html.Span(':関西電力'),
                        ], style={'line-height': '100%'}),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#FFD700"}),
                            html.Span(':中国電力'),
                        ], style={'line-height': '100%'}),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#FFDAB9"}),
                            html.Span(':四国電力'),
                        ], style={'line-height': '100%'}),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#FFB6C1"}),
                            html.Span(':九州電力'),
                        ], style={'line-height': '100%'}),
                    html.H2(
                        [
                            html.Span("■ ", style={"color": "#008B8B"}),
                            html.Span(':沖縄電力'),
                        ])], style={'padding': '5%'})
            ], style={'display': 'flex'}),




            html.Div([html.P(
                html.Details([html.Summary('でんき予報ってなに？'),
                              'でんき予報は、日本の電力会社が提供する電力需給状況の予測データのことである。電力不足が懸念される時期に、ピーク時の供給力と需要予測値を知らせて需給見通しを予報する。', html.Br(),
                              '日々の電気の使用状況や各社の供給力の実績についてわかりやすく伝えることを目的にしている。'])),

                      html.Details([html.Summary('使用したデータについて'),
                                    '今回のダッシュボード作成で扱ったデータはでんき予報の使用電力実績を集計したものである。また、それぞれ各社から同じように使用電力を収集し、3年分のデータとして集計を行った。', html.Br(),
                                    '今後もデータの更新を行っていき、日々新しいデータの統計が行えるようにしていく。']),

                      html.Details([html.Summary('データの更新状況'),
                                    '2022/11/16現在の更新状況↓', html.Br(),
                                    '2022/9/25までのデータを集計済。']),
                      html.Details([html.Summary('電力会社のホームページ'),
                                    '各電気会社へのリンク', html.Br(),
                                    'クリックして詳細をチェック', html.Br(),
                                    html.A('北海道電力', href='http://www.hepco.co.jp'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='https://denkiyoho.hepco.co.jp/area_forecast.html'), html.Br(),
                          html.A('東北電力', href='https://www.tohoku-epco.co.jp'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='https://setsuden.nw.tohoku-epco.co.jp/graph.html'), html.Br(),
                          html.A('東京電力', href='https://www.tepco.co.jp/index-j.html'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='https://www.tepco.co.jp/forecast/'), html.Br(),
                          html.A('北陸電力', href='http://www.rikuden.co.jp'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='http://www.rikuden.co.jp/nw/denki-yoho/index.html'), html.Br(),
                          html.A('中部電力', href='https://www.chuden.co.jp'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='https://powergrid.chuden.co.jp/denkiyoho/'), html.Br(),
                          html.A('関西電力', href='https://www.kansai-td.co.jp/'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='https://www.kansai-td.co.jp/denkiyoho/'), html.Br(),
                          html.A('中国電力', href='https://www.energia.co.jp'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='https://www.energia.co.jp/nw/jukyuu/'), html.Br(),
                          html.A('四国電力', href='https://www.yonden.co.jp'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='https://www.yonden.co.jp/nw/denkiyoho/index.html'), html.Br(),
                          html.A('九州電力', href='https://www.kyuden.co.jp'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='https://www.kyuden.co.jp/td_power_usages/pc.html'), html.Br(),
                          html.A('沖縄電力', href='http://www.okiden.co.jp'), '  データの取得はこちら→', html.A(
                          'でんき予報', href='http://www.okiden.co.jp/denki2/'), html.Br()
                      ])])





        ])

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
                            dcc.Dropdown(id='my-cat-picker', multi=False, value='1day',
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
                                   style={'margin-top': '16px', 'margin-bottom': '4px'},),
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
   
    return  dbc.Container([
            dbc.Row(
                [
                    dbc.Col(sidebar,  className='bg-primary')

                ], style={"height": "35vh"}),
                 ], fluid=True)
        

def heatmap(start_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
    gh = df[(df['DATETIME'] == start_date)]  #表示する日付抽出
    df1 = pd.merge(df1, gh[['エリア', '合計']], on='エリア')#合計を追加していく

    max= df1['合計'].max()
    df1['v'] =df1['合計']/max
    
    df1= df1.set_index('都道府県')
    
    cmap = plt.get_cmap('Blues')
    norm = plt.Normalize(vmin=0, vmax=df1['v'].max())
    fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()
    
    plt.rcParams['figure.figsize'] = 10, 10
    plt.colorbar(plt.cm.ScalarMappable(norm, cmap))
    plt.imshow(picture(df1['v'].apply(fcol)))
    plt.title('電力会社ごと1日の合計使用電力')





if __name__ == '__main__':
    app.run_server(debug=True)
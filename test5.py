import plotly.figure_factory as ff
import plotly.graph_objects as go
import itertools
import japanize_matplotlib
from japanmap import picture
import matplotlib.pyplot as plt
from dash import Dash, html, dcc
import dash
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import folium
from folium.features import CustomIcon
from PIL import Image, ImageDraw, ImageFilter
import pandas as pd
import os
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.use('agg')

# 電力データ
df1 = pd.read_csv("csv/areamap.csv")

drop_down = ['1day', '1month', 'Time']
if drop_down == '1day':
    df = pd.read_csv("csv/1day_kwh.csv")
else:
    df = pd.read_csv("csv/1month_kwh.csv")

company = [k for k, i in itertools.groupby(df['エリア'])]

df3 = pd.read_csv("csv/1day_kwh.csv")
markp = []
markp = df3['DATE']
markp_d = {i: markp[i] for i in range(0, 1000, 166)}


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
# app = Dash(__name__)

app.title = '電力データマップ'
app.layout = html.Div([
    html.H4(children='electric power datemap'),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab([html.Div([
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
                            dcc.Dropdown(id='my-cat-picker', multi=False, value=('1day'),
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
                            dcc.DatePickerRange(id='date',
                                                min_date_allowed=datetime(
                                                    2020, 1, 1),
                                                max_date_allowed=datetime(
                                                    2022, 9, 25),
                                                start_date=datetime(
                                                    2022, 1, 1),
                                                end_date=datetime(2022, 9, 25)
                                                ),
                            html.P(
                                html.Button(id='my-button', n_clicks=0, children='apply',
                                            style={'margin-top': '8px', },
                                            className='bg-dark text-white'
                                            ),
                            ),

                            html.P([
                                html.Label("Time Period",
                                           style={'margin-top': '8px',
                                                  'margin-bottom': '4px'},
                                   className='font-weight-bold'),
                                dcc.RangeSlider(id='slider',
                                                marks=markp_d,
                                                min=0,
                                                max=1000,
                                                # 今回の入力値(初期値)
                                                value=[731, 998],
                                                className='text-dark bg-white '),
                            ],
                            ),

                        ]),
                            # className='bg-secondary text-white'

                        ], style={"height": "25vh"}
                    )
                ], className='bg-primary')

        ]),

            html.Div([
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P('arrow map 入力した日付期間の比較'),
                                html.Div(id='japan_marker')
                            ],
                            # className='bg-white'
                        ),
                        dbc.Col(
                            [
                                html.P('heat_map'),
                                html.Div(id='heat_map'),
                                # html.Img(src=app.get_asset_url("heatmap.png"), alt='plot')
                            ]
                            # className='bg-dark text-white'
                        )
                    ],
                    style={"height": "65vh"}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P('power linegraph'),
                                dcc.Graph(id='linegraph', figure={})
                            ],
                            # className='bg-light'
                        )
                    ],
                    style={"height": "50vh"}
                )
            ], className='bg-dark')
        ], label='dshboard', value='tab-1'),
        dcc.Tab([html.Div([
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
                            dcc.Dropdown(id='my-cat-picker2', multi=False, value='1day',
                                         options=[{'label': x, 'value': x}
                                                  for x in drop_down],
                                         style={'width': '120px'}
                                         ),
                            html.P('Select The companies',
                                   style={'margin-top': '16px',
                                          'margin-bottom': '4px'},
                                   className='font-weight-bold'),
                            dcc.Dropdown(id='my-corr-picker2', multi=True,
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
                            dcc.DatePickerRange(id='date2',
                                                min_date_allowed=datetime(
                                                    2019, 1, 1),
                                                max_date_allowed=datetime(
                                                    2022, 9, 25),
                                                start_date=datetime(
                                                    2022, 1, 1),
                                                end_date=datetime(2022, 9, 25)
                                                ),

                            html.P(
                                html.Button(id='my-button2', n_clicks=0, children='apply',
                                            style={'margin-top': '16px'},
                                            className='bg-dark text-white'
                                            ),
                            )
                        ]),
                            # className='bg-secondary text-white'

                        ], style={"height": "25vh"}
                    )
                ], className='bg-primary')

        ])
        ], label='detail', value='tab-2'),
        dcc.Tab(label='electric company', value='tab-3')

    ]),
    html.Div(id='tabs-example-content'),
    # html.Div(id='heat_map'),
    # html.Div(id='japanmarker')
])


# prevent_initial_call=True
@ app.callback(Output('tabs-example-content', 'children'), Input('tabs-example', 'value'),)
def render_content(tab):
    if tab == 'tab-1':
        content = html.P('                       ')
        return dbc.Container([

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
        return dbc.Container([

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


@ app.callback(Output('heat_map',  'children'), [Input('slider', 'value'), Input('my-button', 'n_clicks'), ], State('date', 'start_date'))
def heatmap(s, n_clicks, start_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if selected_id == 'my-button':
        start = start_date
    # start = datetime.strptime(start_date[:10], '%Y-%m-%d') 時間もでる

        df = pd.read_csv("csv/1day_kwh.csv")
        df1 = pd.read_csv("csv/areamap.csv")

        df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
        gh = df[(df['DATETIME'] == start)]  # 表示する日付抽出

        df1 = pd.merge(df1, gh[['エリア', '合計']], on='エリア')  # 合計を追加していく

        max = df1['合計'].max()
        df1['v'] = df1['合計']/max

        df1 = df1.set_index('都道府県')

        cmap = plt.get_cmap('Blues')
        norm = plt.Normalize(vmin=0, vmax=df1['v'].max())
        def fcol(x): return '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()

        plt.colorbar(plt.cm.ScalarMappable(norm, cmap))

        # plt.cm.ScalarMappable(norm, cmap)

        plt.imshow(picture(df1['v'].apply(fcol)))
        plt.title('電力会社ごと1日の合計使用電力   'f"日付: {start}")
        plt.savefig('assets/heatmap2.png')
        plt.close()
        im2 = Image.open('assets/heatmap2.png')
        im2.save('assets/heatmap3.png')
        im3 = 'assets/heatmap3.png'
        return html.Img(src=Image.open(im3), alt='plot')

    if selected_id == 'slider':
        start = pd.to_datetime(markp[s].astype(str))

        df = pd.read_csv("csv/1day_kwh.csv")
        df1 = pd.read_csv("csv/areamap.csv")

        df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
        gh = df[(df['DATETIME'] == start[s[0]])]  # 表示する日付抽出

        df1 = pd.merge(df1, gh[['エリア', '合計']], on='エリア')  # 合計を追加していく

        max = df1['合計'].max()
        df1['v'] = df1['合計']/max

        df1 = df1.set_index('都道府県')

        cmap = plt.get_cmap('Blues')
        norm = plt.Normalize(vmin=0, vmax=df1['v'].max())
        def fcol(x): return '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()

        plt.colorbar(plt.cm.ScalarMappable(norm, cmap))

        # plt.cm.ScalarMappable(norm, cmap)
        title = markp[s[0]]
        plt.imshow(picture(df1['v'].apply(fcol)))
        plt.title('電力会社ごと1日の合計使用電力   'f"日付: {title}")
        plt.savefig('assets/heatmap2.png')
        plt.close()
        im2 = Image.open('assets/heatmap2.png')
        im2.save('assets/heatmap3.png')
        im3 = 'assets/heatmap3.png'
        return html.Img(src=Image.open(im3), alt='plot')


'''
@ app.callback(Output('linegraph', 'figure'),
               [Input('slider', 'value'), Input('my-button', 'n_clicks'), ],
               [State('my-corr-picker', 'value'),
               State('my-cat-picker', 'value'),
               State('date', 'start_date'),
               State('date', 'end_date')])
def linegraph(n_clicks, s, corr_pick, value, start_date, end_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if selected_id == 'my-button':
        start = start_date
        end = end_date

        drop_down = value
        if drop_down == '1day':
            df = pd.read_csv("csv/1day_kwh.csv")
            df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
        elif drop_down == '1month':
            df = pd.read_csv("csv/1month_kwh.csv")
            df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
        else:
            df = pd.read_csv("csv/time_kwh.csv")
        # + df['TIME'].astype(str))
            df['DATETIME'] = pd.to_datetime(df['DATETIME'].astype(str))

    # df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))

        gh = df[(df['DATETIME'] >= start) & (
            df['DATETIME'] <= end)]  # 表示する期間のみ抽出

        strPC = [str(num) for num in corr_pick]

        xaxis = go.layout.XAxis(title='日付')
        yaxis = go.layout.YAxis(title='万kw')

        fig = go.Figure(layout=go.Layout(
            title="Power Line Plot  "f"期間: {start} - {end}", xaxis=xaxis, yaxis=yaxis))

        if 'tokyo' in corr_pick:
            tokyo = gh[gh['エリア'] == 'tokyo']
            fig.add_trace(go.Scatter(
                x=list(tokyo['DATETIME']),
                y=list(tokyo['合計']),
                name="tokyo"))

        if 'kansai' in corr_pick:
            kansai = gh[gh['エリア'] == 'kansai']
            fig.add_trace(go.Scatter(
                x=kansai['DATETIME'],
                y=kansai['合計'], name="kansai"))

        if 'chubu' in corr_pick:
            chubu = gh[gh['エリア'] == 'chubu']
            fig.add_trace(go.Scatter(
                x=chubu['DATETIME'],
                y=chubu['合計'], name="chubu"))

        if 'tohoku' in corr_pick:
            tohoku = gh[gh['エリア'] == 'tohoku']
            fig.add_trace(go.Scatter(
                x=tohoku['DATETIME'],
                y=tohoku['合計'], name="tohoku"))

        if 'chugoku' in corr_pick:
            chugoku = gh[gh['エリア'] == 'chugoku']
            fig.add_trace(go.Scatter(
                x=chugoku['DATETIME'],
                y=chugoku['合計'], name="chugoku"))

        return fig

    if selected_id == 'slider':
        date = pd.to_datetime(markp[s].astype(str))
        drop_down = value
        if drop_down == '1day':
            df = pd.read_csv("csv/1day_kwh.csv")
            df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
        elif drop_down == '1month':
            df = pd.read_csv("csv/1month_kwh.csv")
            df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
        else:
            df = pd.read_csv("csv/time_kwh.csv")
        # + df['TIME'].astype(str))
            df['DATETIME'] = pd.to_datetime(df['DATETIME'].astype(str))
        gh = df[(df['DATETIME'] >= date[s[0]]) & (
        df['DATETIME'] <= date[s[1]])]  # 表示する期間のみ抽出
        start = markp[s[0]]
        end = markp[s[1]]

        strPC = [str(num) for num in corr_pick]

        xaxis = go.layout.XAxis(title='日付')
        yaxis = go.layout.YAxis(title='万kw')

        fig = go.Figure(layout=go.Layout(
            title="Power Line Plot  "f"期間: {start} - {end}", xaxis=xaxis, yaxis=yaxis))

        if 'tokyo' in corr_pick:
            tokyo = gh[gh['エリア'] == 'tokyo']
            fig.add_trace(go.Scatter(
                x=list(tokyo['DATETIME']),
                y=list(tokyo['合計']),
                name="tokyo"))

        if 'kansai' in corr_pick:
            kansai = gh[gh['エリア'] == 'kansai']
            fig.add_trace(go.Scatter(
                x=kansai['DATETIME'],
                y=kansai['合計'], name="kansai"))

        if 'chubu' in corr_pick:
            chubu = gh[gh['エリア'] == 'chubu']
            fig.add_trace(go.Scatter(
                x=chubu['DATETIME'],
                y=chubu['合計'], name="chubu"))

        if 'tohoku' in corr_pick:
            tohoku = gh[gh['エリア'] == 'tohoku']
            fig.add_trace(go.Scatter(
                x=tohoku['DATETIME'],
                y=tohoku['合計'], name="tohoku"))

        if 'chugoku' in corr_pick:
            chugoku = gh[gh['エリア'] == 'chugoku']
            fig.add_trace(go.Scatter(
                x=chugoku['DATETIME'],
                y=chugoku['合計'], name="chugoku"))

        return fig



'''


@ app.callback(Output('linegraph', 'figure'),
               [Input('slider', 'value'), Input('my-button', 'n_clicks'),],
               [State('my-corr-picker', 'value'),
               State('my-cat-picker', 'value'),
               State('date', 'start_date'),State('date', 'end_date')
                ])
def linegraph(s,n_clicks, corr_pick, value, start_date, end_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    drop_down = value
    if drop_down == '1day':
        df = pd.read_csv("csv/1day_kwh.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
    elif drop_down == '1month':
        df = pd.read_csv("csv/1month_kwh.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
    else:
        df = pd.read_csv("csv/time_kwh.csv")
        # + df['TIME'].astype(str))
        df['DATETIME'] = pd.to_datetime(df['DATETIME'].astype(str))

    #df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))

    if selected_id == 'slider':
        date = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] >= date[s[0]]) & (
        df['DATETIME'] <= date[s[1]])]  # 表示する期間のみ抽出
        start = markp[s[0]]
        end = markp[s[1]]

    if selected_id == 'my-button':
        start = start_date
        end = end_date
        gh = df[(df['DATETIME'] >= start) & (
            df['DATETIME'] <= end)] 

    strPC = [str(num) for num in corr_pick]

    xaxis = go.layout.XAxis(title='日付')
    yaxis = go.layout.YAxis(title='万kw')

    
    fig = go.Figure(layout=go.Layout(
        title="Power Line Plot  "f"期間: {start} - {end}", xaxis=xaxis, yaxis=yaxis))

    if 'tokyo' in corr_pick:
        tokyo = gh[gh['エリア'] == 'tokyo']
        fig.add_trace(go.Scatter(
            x=list(tokyo['DATETIME']),
            y=list(tokyo['合計']),
            name="tokyo"))

    if 'kansai' in corr_pick:
        kansai = gh[gh['エリア'] == 'kansai']
        fig.add_trace(go.Scatter(
            x=kansai['DATETIME'],
            y=kansai['合計'], name="kansai"))

    if 'chubu' in corr_pick:
        chubu = gh[gh['エリア'] == 'chubu']
        fig.add_trace(go.Scatter(
            x=chubu['DATETIME'],
            y=chubu['合計'], name="chubu"))

    if 'tohoku' in corr_pick:
        tohoku = gh[gh['エリア'] == 'tohoku']
        fig.add_trace(go.Scatter(
            x=tohoku['DATETIME'],
            y=tohoku['合計'], name="tohoku"))

    if 'chugoku' in corr_pick:
        chugoku = gh[gh['エリア'] == 'chugoku']
        fig.add_trace(go.Scatter(
            x=chugoku['DATETIME'],
            y=chugoku['合計'], name="chugoku"))

    return fig


@app.callback(Output('japan_marker', 'children'),
             [Input('slider', 'value'), Input('my-button', 'n_clicks'),],
              State('date', 'start_date'),
              State('date', 'end_date'))
def japanmarker(s,n_clicks, start_date, end_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    df = pd.read_csv("csv/1day_kwh.csv")
    df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))

    if selected_id == 'slider':
        date = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] >= date[s[0]]) & (
        df['DATETIME'] <= date[s[1]])]  # 表示する期間のみ抽出
        start = markp[s[0]]
        end = markp[s[1]]

    if selected_id == 'my-button':
        start = start_date
        end = end_date
        gh = df[(df['DATETIME'] >= start) & (
            df['DATETIME'] <= end)]
    
    
    map = folium.Map([36.95538513720449, 138.87388736292712],
                     tiles="OpenStreetMap", zoom_start=5.45)

    # 東京電力
    dfs1 = gh[gh['エリア'] == 'tokyo']
    s1 = dfs1['合計'].iloc[0]  # 最初の合計値
    e1 = dfs1['合計'].iloc[-1]  # 最後の合計値
    if s1 > e1:
        comp = s1 - e1
        popup = folium.Popup(f"{comp}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      35.670129705913446, 139.75842700498842], icon=icon, popup=popup).add_to(map)
    else:
        comp = e1 - s1
        popup = folium.Popup(f"{comp}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      35.670129705913446, 139.75842700498842], icon=icon, popup=popup).add_to(map)

    # 関西電力
    dfs2 = gh[gh['エリア'] == 'kansai']
    s2 = dfs2['合計'].iloc[0]  # 最初の合計値
    e2 = dfs2['合計'].iloc[-1]  # 最後の合計値
    if s2 > e2:
        comp_down = s2 - e2
        popup = folium.Popup(f"{comp_down}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      34.69252759139264, 135.49243297974868], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e2 - s2
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      34.69252759139264, 135.49243297974868], icon=icon, popup=popup).add_to(map)

    # 中部電力
    dfs3 = gh[gh['エリア'] == 'chubu']
    s3 = dfs3['合計'].iloc[0]  # 最初の合計値
    e3 = dfs3['合計'].iloc[-1]  # 最後の合計値
    if s3 > e3:
        comp_down = s3 - e3
        popup = folium.Popup(f"{comp_down}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      35.17155442553177, 136.91379246511167], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e3 - s3
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      35.17155442553177, 136.91379246511167], icon=icon, popup=popup).add_to(map)

    # 東北電力
    dfs4 = gh[gh['エリア'] == 'tohoku']
    s4 = dfs4['合計'].iloc[0]  # 最初の合計値
    e4 = dfs4['合計'].iloc[-1]  # 最後の合計値
    if s4 > e4:
        comp_down = s4 - e4
        popup = folium.Popup(f"{comp_down}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      38.298699791215576, 140.87768450198496], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e4 - s4
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      38.298699791215576, 140.87768450198496], icon=icon, popup=popup).add_to(map)

    # 中国電力
    dfs5 = gh[gh['エリア'] == 'chugoku']
    s5 = dfs5['合計'].iloc[0]  # 最初の合計値
    e5 = dfs5['合計'].iloc[-1]  # 最後の合計値
    if s5 > e5:
        comp_down = s5 - e5
        popup = folium.Popup(f"{comp_down}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      34.388644834151, 132.45569865610997], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e5 - s5
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="/Users/mie.tooyama/web/images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      34.388644834151, 132.45569865610997], icon=icon, popup=popup).add_to(map)

    map.save('compmap.html')
    new = 'compmap.html'
    return html.Iframe(srcDoc=open(new, 'r').read(), width='100%', height='550')


#raise dash.exceptions.PreventUpdate
if __name__ == '__main__':
    app.run_server(debug=False)

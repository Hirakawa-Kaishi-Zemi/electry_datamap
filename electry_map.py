import itertools
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import folium
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from dash import html, dcc
from dash.dependencies import Input, Output, State
from folium.features import CustomIcon
from japanmap import picture
from plotly.subplots import make_subplots

matplotlib.use('agg')

# 電力データ

df1 = pd.read_csv("csv/1day_kwh.csv") 
markp = []
markp = df1['DATE']
markp_d = {i: markp[i] for i in range(0, 10000, 1000)}
#統計範囲、期間の設定
drop_down = ['1day', '1month', 'Time']
#発電方法の選択
drop_down2 = ['火力', '水力', '太陽光','バイオマス','風力','原子力','地熱']
#日本の各電力会社
company = [k 
for k, i in itertools.groupby(df1['エリア'])] #####


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
# app = Dash(__name__)

app.title = '電力データマップ'
app.layout = html.Div([
    #タイトル
    html.H2(children='electric power datemap',className='bg-primary'),
    
    dcc.Tabs(id='tabs-example', value='tab-2', children=[
        #タブ2の中身
        dcc.Tab([html.Div([
            dbc.Row(
                [
                    html.H4('Settings',
                            style={'margin-top': '10px', 'margin-left': '15px'})

                ], style={"height": "5vh"}, className='bg-primary text-white font-italic'
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [html.Div([
                            #統計範囲、期間の選択
                            html.H5('データの範囲選択',
                                   style={'margin-top': '30px',
                                          'margin-bottom': '5px', 'left': '10px'},
                                   ),
                                   #初期値は1dayで、繋げるためにはidを指定
                            dcc.Dropdown(id='my-cat-picker', multi=False, value=('1day'),
                                         options=[{'label': x, 'value': x}
                                                  for x in drop_down],
                                         style={'width': '120px',
                                             'left': '10px'},#,'background':'#4169e1'
                                          className='btn btn-outline-info'#className='font-weight-bold nav-item dropdown
                                         ),
                        ])
                        ]),
                        dbc.Col([html.H5('日付期間の選択',
                                   style={'margin-top': '30px', 'margin-bottom': '4px', 'left': '10px'},),
                            dcc.DatePickerRange(id='date',
                                                min_date_allowed=datetime(
                                                    2019, 4, 1),
                                                max_date_allowed=datetime(
                                                    2023, 10, 31),
                                                start_date=datetime(
                                                    2020, 1, 1),
                                                end_date=datetime(2022, 1, 1)
                        ),]

                        ),

                    dbc.Col(
                        [
                            #日本の各電力会社の選択、複数選択可能
                            html.H5('日本の各電力会社の選択',
                                   style={'margin-top': '30px',
                                          'margin-bottom': '4px', 'left': '10px'},
                                   className='font-weight-bold'),
                            dcc.Dropdown(id='my-corr-picker', multi=True,
                                         value=company,
                                         options=[{'label': x, 'value': x}
                                                  for x in company],
                                         #style={'width': '450px','right': '100px'  # 'color': '#8800e3','border-color': '#8800e3',#'background-color':'#9d18f5',
                                        #},
                                         className='btn btn-outline-info'
                                         ),  
                            #実行ボタン、上記３つで決定したものはこのボタンで反映される
                            
                            # className='bg-secondary text-white'

                        ], style={"height": "25vh"}
                    ),
                    dbc.Row(html.Div([html.H5(
                                html.Button(id='my-button', n_clicks=0, children='apply',
                                            style={'margin-top': '20px',
                                                'left': '5px','align':'center'},
                                            className='btn btn-outline-success' ###
                                            ),
                            ),
                        ]),
                    ),
                    #スライドバーで期間の選択、実行ボタンなしでグラフ表示
                    html.H5([
                                html.Label("日付期間の選択",
                                           style={'margin-top': '8px',
                                                  'margin-bottom': '4px'},
                                   className='font-weight-bold'),
                                dcc.RangeSlider(id='slider',
                                                marks=markp_d,
                                                min=0,
                                                max=5000,
                                                # 今回の入力値(初期値)
                                                value=[731, 998],
                                                className='font-weight-bold form-range'), ###
                            ],
                            ),

                ],)

        ]),

            html.Div([
                        #折れ線グラフ
                dbc.Row(
                    [
                        dbc.Col(
                            [
                               # html.P('power linegraph'),
                                dcc.Graph(id='linegraph', figure={})
                            ],
                            # className='bg-light'
                        )
                    ],
                    style={"height": "55vh"}
                ), #矢印マップのとなりはエリア別発電量
                        dbc.Row([
                            dbc.Col(
                            [
                                html.H4('入力した日付期間の比較',style={'margin-top': '30px',
                                          'margin-bottom': '5px', 'left': '10px'},),
                                html.Div(id='japan_marker',style={'margin-top': '50px', })
                            ],#style={"height": "90vh",},
                            # className='bg-white' 
                           
                       ),
                         #円で各発電ごとの発電量の比較
                        dbc.Col(
                    [
                        html.H4('エリアごと発電方式別発電量',style={'margin-top': '30px',
                                          'margin-bottom': '5px', 'left': '10px'},),#power ratio
                        html.Div([
                            html.H5('発電方式の選択',
                                   style={'margin-top': '8px',
                                          'margin-bottom': '4px', 'left': '10px'},
                                   className='font-weight-bold'),
                                   #初期値は火力、ドロップダウンで選択可能、一つだけ
                            dcc.Dropdown(id='pg', multi=False, value=('火力'),
                                         options=[{'label': x, 'value': x}
                                                  for x in drop_down2],
                                         style={'width': '120px',
                                             'left': '10px'}
                                         ),
                            ##セッティングにドロップダウン持っていく
                
                            ]),
                        
                        html.Div(id='kyokyu_marker')
                        
                    ])
                    ]
                    # className='bg-white'
                    ),
                dbc.Row(
                [   
#円グラフ全ての会社を表示（選択で見たい会社のみもできる）
                 dbc.Col(
                        [
                            html.P(''),
                            dcc.Graph(id='pie_chart',figure={}),
                        ],
                        # className='bg-light'
                    )
                ],
                style={"height": "90vh",}
                        
                ),
                #すぐ下に棒グラフ表示　上の円グラフと同じ
                dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P(''),
                            dcc.Graph(id='bar_chart',figure={}),
                        ],
                        # className='bg-light'
                    )
                ],
               style={"height": "100vh",}
                ),
                        ],)
            # className='bg-dark'
        ], className='', label='電力統計', value='tab-2'),
       
        
       
       
        #タブ3の中身
        dcc.Tab([ 
                html.Div([

            html.H1('電力統計のグラフについて'),

            html.Div([html.P(
                html.Details([html.Summary('電力使用量の折れ線グラフ'),
                              '特定の期間内での電力消費のトレンドやパターンを把握することができる。'])),

                      html.P(html.Details([html.Summary('電力使用量の増減グラフ'),
                                    '直感的に増減を見ることができ、地域の違いを把握することができる。'])),

                      html.P(html.Details([html.Summary('発電電力量割合の円グラフ'),
                                           '特定の日で各電力会社の発電電力量の割合、発電方式の変化を見ることができる。'])),

                      html.P(html.Details([html.Summary('発電電力量の棒グラフ'),
                                    '円グラフと共に実際の発電電力量を示すことで発電量の具体的な数値を把握することができる。'])),

                      html.P(html.Details([html.Summary('エリアごと発電方式別発電量円グラフ'),
                                    '日本地図にプロットすることで視覚的に発電量を把握できる。'])),

                    html.P(html.Details([html.Summary('電力需給予測のグラフ'),
                                    '発電量と需要量のバランスを視覚化することでピーク時の需要供給の調整や需要制御の重要性を把握できる。'])),

            html.Div([html.H5('グラフの書き出し'),
                     html.H5('chatGPTを使ったグラフのカスタマイズ'),

                     
            ])

             ])
        ], )#className='bg-dark'
    ], label = 'グラフについて', value = 'tab-3'),
#概要
    dcc.Tab([
        html.Div([

            html.H1('電力データマップについて'),

            html.H5(' この電力データマップは日本の電力会社（10社）の電力に関するデータを集め、可視化したものである。近年の電気代値上がりや気候変動による電力逼迫など、日本社会で電力に関する問題が顕著になってきた。この電力危機を脱するために、企業で何ができるだろうか。'),
            html.H5(' 電力のデータに触れ、現状を把握、分析を行い対策を講じていくことが今後必要になると考える。そのためにも、各電力会社の情報をまとめて見ることができるこの電力データマップを役立ててほしい。'),

            html.Div([html.Img(src=app.get_asset_url("colormap.png"),
                     alt='japan', style={'display': 'inline-block'}),

                html.Div([
                    html.H3('<凡例>'),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#9966CC"}),
                            html.Span(':北海道電力')
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#87CEFA"}),
                            html.Span(':東北電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#B0E0E6"}),
                            html.Span(':東京電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#808080"}),
                            html.Span(':北陸電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#98FB98"}),
                            html.Span(':中部電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#9ACD32"}),
                            html.Span(':関西電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#FFD700"}),
                            html.Span(':中国電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#FFDAB9"}),
                            html.Span(':四国電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#FFB6C1"}),
                            html.Span(':九州電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#008B8B"}),
                            html.Span(':沖縄電力'),
                        ])], style={'padding': '5%'})
            ], style={'display': 'flex'}),


            html.Div([html.P(
                html.Details([html.Summary('でんき予報ってなに？'),
                              'でんき予報は、日本の電力会社が提供する電力需給状況の予測データのことである。電力不足が懸念される時期に、ピーク時の供給力と需要予測値を知らせて需給見通しを予報する。', html.Br(),
                              '日々の電気の使用状況や各社の供給力の実績についてわかりやすく伝えることを目的にしている。'])),

                      html.P(html.Details([html.Summary('使用したデータについて'),
                                    '今回のダッシュボード作成で扱ったデータはでんき予報の使用電力実績を集計したものである。また、それぞれ各社から同じように使用電力を収集し、3年分のデータとして集計を行った。', html.Br(),
                                    '他にも発電方式別にどれくらいの量が発電されているかなど、それぞれの発電所における発電電力量も集計している。今後もデータの更新を行っていき、日々新しいデータの統計が行えるようにしていく。'])),

                      html.P(html.Details([html.Summary('使用データの公開'),
                                           'ここでは電力統計で使われている電力データをダウンロードすることが可能である。ただし、元データを加工したものであるため、元データの取得は各電力会社HPより取得してください。', html.Br(),
                                           'csvファイル', html.Br(),
                                           'グラフのカスタムなどは「グラフについて」より行ってください。'])),

                      html.P(html.Details([html.Summary('データの更新状況'),
                                    '2022/11/16現在の更新状況↓', html.Br(),
                                    '2022/9/25までのデータを集計済。'])),

                      html.P(html.Details([html.Summary('電力会社のホームページ'),
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
                      ]))
                      ])
        ])
    ],label = '概要', value = 'tab-1')
]),html.Div(id='tabs-example-content'),])
# prevent_initial_call=True
@ app.callback(Output('tabs-example-content', 'children'), Input('tabs-example', 'value'),)
def render_content(tab):
    # いらないかも
    if tab == 'tab-3':
        content=html.P('                       ')
        return dbc.Container([

            dbc.Row(
                [
                    dbc.Col(content, )
                ]),
        ], fluid=True)

    elif tab == 'tab-2':
        content=html.P('                       ')
        return dbc.Container([

            
        ], fluid=True)
    elif tab == 'tab-1':
        #タブ1の中身　表示
        return html.Div([

            html.H1('電力データマップについて'),

            html.Div([html.H5('この電力データマップは日本の電力会社（10社）の電力に関するデータを集め、可視化したものである。近年の電気代値上がりや気候変動による電力逼迫など、日本社会で電力に関する問題が顕著になってきた。この電力危機を脱するために、企業で何ができるだろうか。', html.Br(),'電力のデータに触れ、現状を把握、分析を行い対策を講じていくことが今後必要になると考える。そのためにも、各電力会社の情報をまとめて見ることができるこの電力データマップを役立ててほしい。')]),

            html.Div([html.Img(src=app.get_asset_url("colormap.png"),
                     alt='japan', style={'display': 'inline-block'}),

                html.Div([
                    html.H3('<凡例>'),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#9966CC"}),
                            html.Span(':北海道電力')
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#87CEFA"}),
                            html.Span(':東北電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#B0E0E6"}),
                            html.Span(':東京電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#808080"}),
                            html.Span(':北陸電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#98FB98"}),
                            html.Span(':中部電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#9ACD32"}),
                            html.Span(':関西電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#FFD700"}),
                            html.Span(':中国電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#FFDAB9"}),
                            html.Span(':四国電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#FFB6C1"}),
                            html.Span(':九州電力'),
                        ], style={'line-height': '100%'}),
                    html.H4(
                        [
                            html.Span("■ ", style={"color": "#008B8B"}),
                            html.Span(':沖縄電力'),
                        ])], style={'padding': '5%'})
            ], style={'display': 'flex'}),


            html.Div([html.P(
                html.Details([html.Summary('でんき予報ってなに？'),
                              'でんき予報は、日本の電力会社が提供する電力需給状況の予測データのことである。電力不足が懸念される時期に、ピーク時の供給力と需要予測値を知らせて需給見通しを予報する。', html.Br(),
                              '日々の電気の使用状況や各社の供給力の実績についてわかりやすく伝えることを目的にしている。'])),

                      html.P(html.Details([html.Summary('使用したデータについて'),
                                    '今回のダッシュボード作成で扱ったデータはでんき予報の使用電力実績を集計したものである。また、それぞれ各社から同じように使用電力を収集し、3年分のデータとして集計を行った。', html.Br(),
                                    '他にも発電方式別にどれくらいの量が発電されているかなど、それぞれの発電所における発電電力量も集計している。今後もデータの更新を行っていき、日々新しいデータの統計が行えるようにしていく。'])),

                      html.P(html.Details([html.Summary('使用データの公開'),
                                           'ここでは電力統計で使われている電力データをダウンロードすることが可能である。ただし、元データを加工したものであるため、元データの取得は各電力会社HPより取得してください。', html.Br(),
                                           'csvファイル', html.Br(),
                                           'グラフのカスタムなどは「グラフについて」より行ってください。'])),

                      html.P(html.Details([html.Summary('データの更新状況'),
                                    '2022/11/16現在の更新状況↓', html.Br(),
                                    '2022/9/25までのデータを集計済。'])),

                      html.P(html.Details([html.Summary('電力会社のホームページ'),
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
                      ]))
                      ])


        ])


@ app.callback(Output('heat_map',  'children'), [Input('slider', 'value'), Input('my-button', 'n_clicks'), ], State('date', 'start_date'))
def heatmap(s, n_clicks, start_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    #データセット
    df = pd.read_csv("csv/1day_kwh.csv")
    df1 = pd.read_csv("csv/areamap.csv")
    
    #データタイムの作成
    df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))

    #ボタンを押した場合の処理　
    if selected_id == 'my-button':
        start = start_date
        gh = df[(df['DATETIME'] == start)]  # 表示する日付抽出
        title = start
    # start = datetime.strptime(start_date[:10], '%Y-%m-%d') 時間もでる

    #スライダーで日付指定した場合の処理
    if selected_id == 'slider':
        start = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] == start[s[0]])]  # 表示する日付抽出
        title = markp[s[0]]

    #エリアごとの合計を追加し、最大値と割合を求める
    df1 = pd.merge(df1, gh[['エリア', '合計']], on='エリア')  # 合計を追加していく
    max = df1['合計'].max()
    df1['v'] = df1['合計']/max

    df1 = df1.set_index('都道府県')
 
    #都道府県ごとに色をつける
    cmap = plt.get_cmap('Blues')
    norm = plt.Normalize(vmin=0, vmax=df1['v'].max())
    def fcol(x): return '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()

    plt.colorbar(plt.cm.ScalarMappable(norm, cmap))

        # plt.cm.ScalarMappable(norm, cmap)

    plt.imshow(picture(df1['v'].apply(fcol)))
    plt.title('電力会社ごと1日の合計使用電力   'f"日付: {title}")
    plt.savefig('assets/heatmap2.png')
    plt.close()
    im2 = Image.open('assets/heatmap2.png')
    im2.save('assets/heatmap3.png')
    im3 = 'assets/heatmap3.png'
    return html.Img(src=Image.open(im3), alt='plot')



@ app.callback(Output('linegraph', 'figure'),
               [Input('slider', 'value'), Input('my-button', 'n_clicks'), ],
               [State('my-corr-picker', 'value'),
               State('my-cat-picker', 'value'),
               State('date', 'start_date'), State('date', 'end_date')
                ])
def linegraph(s, n_clicks, corr_pick, value, start_date, end_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    #どの選択肢を選んだかを判断する処理
    drop_down = value
    if drop_down == '1day':
        df = pd.read_csv("csv/1day_kwh.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'])
    elif drop_down == '1month':
        df = pd.read_csv("csv/1month_kwh.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
    else:
        df = pd.read_csv("csv/time_kwh.csv")
        df['DATETIME'] = pd.to_datetime(df['DATETIME'].astype(str))

    #スライダーの日付を変更したときの処理
    if selected_id == 'slider':
        date = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] >= date[s[0]]) & (
            df['DATETIME'] <= date[s[1]])]  # 表示する期間のみ抽出
        start = markp[s[0]] #グラフタイトルのための変数　最初日
        end = markp[s[1]]  #最終日

    #ボタンを押したときの処理
    if selected_id == 'my-button':
        start = start_date  #入力値を変数に代入
        end = end_date
        gh = df[(df['DATETIME'] >= start) & (
            df['DATETIME'] <= end)] #期間の抽出

    strPC = [str(num) for num in corr_pick]

    #x軸とy軸のタイトル
    xaxis = go.layout.XAxis(title='日付')
    yaxis = go.layout.YAxis(title='万kw')
    
    #グラフの線画
    fig = go.Figure(layout=go.Layout(
        title="電力使用量の推移  "f"期間: {start} - {end}", xaxis=xaxis, yaxis=yaxis))
    
    #選択された各電力会社ごとの折れ線グラフ追加
    if 'tokyo' in corr_pick:
        tokyo = gh[gh['エリア'] == 'tokyo']
        fig.add_trace(go.Scatter(
            x=list(tokyo['DATETIME']),
            y=list(tokyo['合計']),
            name="tokyo"))

    if 'kansai' in corr_pick:
        kansai = gh[gh['エリア'] == 'kansai']
        fig.add_trace(go.Scatter(
            x=list(kansai['DATETIME']),
            y=list(kansai['合計']), name="kansai"))

    if 'chubu' in corr_pick:
        chubu = gh[gh['エリア'] == 'chubu']
        fig.add_trace(go.Scatter(
            x=list(chubu['DATETIME']),
            y=list(chubu['合計']), name="chubu"))

    if 'tohoku' in corr_pick:
        tohoku = gh[gh['エリア'] == 'tohoku']
        fig.add_trace(go.Scatter(
            x=list(tohoku['DATETIME']),
            y=list(tohoku['合計']), name="tohoku"))

    if 'chugoku' in corr_pick:
        chugoku = gh[gh['エリア'] == 'chugoku']
        fig.add_trace(go.Scatter(
            x=list(chugoku['DATETIME']),
            y=list(chugoku['合計']), name="chugoku"))
        
    if 'hokkaido' in corr_pick:
        chugoku = gh[gh['エリア'] == 'hokkaido']
        fig.add_trace(go.Scatter(
            x=list(chugoku['DATETIME']),
            y=list(chugoku['合計']), name="hokkaido"))
        
    if 'hokuriku' in corr_pick:
        chugoku = gh[gh['エリア'] == 'hokuriku']
        fig.add_trace(go.Scatter(
            x=list(chugoku['DATETIME']),
            y=list(chugoku['合計']), name="hokuriku"))
        
    if 'kyushu' in corr_pick:
        chugoku = gh[gh['エリア'] == 'kyushu']
        fig.add_trace(go.Scatter(
            x=list(chugoku['DATETIME']),
            y=list(chugoku['合計']), name="kyushu"))
        
    if 'okinawa' in corr_pick:
        chugoku = gh[gh['エリア'] == 'okinawa']
        fig.add_trace(go.Scatter(
            x=list(chugoku['DATETIME']),
            y=list(chugoku['合計']), name="okinawa"))
        
    if 'sikoku' in corr_pick:
        chugoku = gh[gh['エリア'] == 'sikoku']
        fig.add_trace(go.Scatter(
            x=list(chugoku['DATETIME']),
            y=list(chugoku['合計']), name="sikoku"))

    return fig


@app.callback(Output('japan_marker', 'children'),
              [Input('slider', 'value'), Input('my-button', 'n_clicks'), ],
              State('date', 'start_date'),
              State('date', 'end_date'))
def japanmarker(s, n_clicks, start_date, end_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    #データセットの読み込み、データタイムの作成
    df = pd.read_csv("csv/1day_kwh.csv")
    df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))

    #スライダーを変更したときの処理
    if selected_id == 'slider':
        date = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] >= date[s[0]]) & (
            df['DATETIME'] <= date[s[1]])]  # 表示する期間のみ抽出
        start = markp[s[0]]
        end = markp[s[1]]

    #ボタンでセッティングを変更したときの処理
    if selected_id == 'my-button':
        start = start_date
        end = end_date
        gh = df[(df['DATETIME'] >= start) & (
            df['DATETIME'] <= end)]

    #初期値の座標を設定して、日本地図の中心を決める
    map = folium.Map([36.95538513720449, 138.87388736292712],
                     tiles="OpenStreetMap", zoom_start=5.45)


    #電力会社ごとに入力した日付の比較を行う。減少した場合には矢印は下向きに、増加した場合は上向きになる処理
    #矢印は画像から参照、座標は電力会社の本社があるところ
    # 東京電力
    dfs1 = gh[gh['エリア'] == 'tokyo']
    s1 = dfs1['合計'].iloc[0]  # 最初の合計値
    e1 = dfs1['合計'].iloc[-1]  # 最後の合計値
    if s1 > e1:#最初の値が大きいときは減少のため下矢印を表示する
        comp = s1 - e1
        popup = folium.Popup(f"{comp}万kw減少", max_width=300) #ポップアップの大きさと表示する文字の指定
        icon = CustomIcon(
            #矢印のパスに注意が必要※
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3)) #アイコンの指定、自分のフォルダの画像を持ってくる
        folium.Marker(location=[#マーカーを示したい座標
                      35.670129705913446, 139.75842700498842], icon=icon, popup=popup).add_to(map)
    else:#それ以外、つまり最初の値が小さいときは増加のため上矢印を表示する
        comp = e1 - s1
        popup = folium.Popup(f"{comp}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
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
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      34.69252759139264, 135.49243297974868], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e2 - s2
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
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
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      35.17155442553177, 136.91379246511167], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e3 - s3
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
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
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      38.298699791215576, 140.87768450198496], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e4 - s4
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
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
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      34.388644834151, 132.45569865610997], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e5 - s5
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      34.388644834151, 132.45569865610997], icon=icon, popup=popup).add_to(map)

    map.save('compmap.html')
    new = 'compmap.html'
    return html.Iframe(srcDoc=open(new, 'r').read(), width='100%', height='550')


@ app.callback(Output('pie_chart',  'figure'), 
[Input('slider', 'value'), Input('my-button', 'n_clicks'), ],
State('my-corr-picker', 'value'),State('my-cat-picker', 'value'), State('date', 'start_date'))
def piechart(s, n_clicks,corr_pick,value,start_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    drop_down = value
    if drop_down == '1day':
        df = pd.read_csv("csv/1day_jukyu.csv") ####
        df['DATETIME'] = pd.to_datetime(df['DATE'])
    elif drop_down == '1month':
        df = pd.read_csv("csv/1month_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
    else:
        df = pd.read_csv("csv/time_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATETIME'].astype(str))

    if selected_id == 'my-button':
        start = start_date
        gh = df[(df['DATETIME'] == start)]  # 表示する日付抽出
        title2 = start
    # start = datetime.strptime(start_date[:10], '%Y-%m-%d') 時間もでる

    if selected_id == 'slider':
        start = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] == start[s[0]])]  # 表示する日付抽出
        title2 = markp[s[0]]
    
    strPC = [str(num) for num in corr_pick]

    #fig = make_subplots(rows=1, cols=5)

#labelの作成が必要　凡例をつくる
    fig = make_subplots(
        rows=2, cols=5,  # 行数と列数
        vertical_spacing=0.1,  # 表とグラフの間の間隔を0に
        specs=[[{"type": "pie"}, {"type": "pie"},{"type": "pie"},{"type": "pie"},{"type": "pie"}],
                [{"type": "pie"}, {"type": "pie"},{"type": "pie"},{"type": "pie"},{"type": "pie"}]],  # subplotするグラフの配置順やグラフの種類
        subplot_titles=['北海道電力','東北電力','中部電力','北陸電力','東京電力',
                        '関西電力', '中国電力', '四国電力', '九州電力','沖縄電力'],
        )
    
    if 'hokkaido' in corr_pick:
        hokkaido = gh[gh['エリア'] == 'hokkaido']
        l1=hokkaido['原子力'].iloc[0]
        l2=hokkaido['火力'].iloc[0]
        l3=hokkaido['水力'].iloc[0]
        l4=hokkaido['地熱'].iloc[0]
        l5=hokkaido['バイオマス'].iloc[0]
        l6=hokkaido['太陽光'].iloc[0]
        l7=hokkaido['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
            name="hokkaido"),row=1, col=1)
 
    if 'tohoku' in corr_pick:
        tohoku = gh[gh['エリア'] == 'tohoku']
        l1=tohoku['原子力'].iloc[0]
        l2=tohoku['火力'].iloc[0]
        l3=tohoku['水力'].iloc[0]
        l4=tohoku['地熱'].iloc[0]
        l5=tohoku['バイオマス'].iloc[0]
        l6=tohoku['太陽光'].iloc[0]
        l7=tohoku['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7] 

        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
               #  marker=dict(colors=['#f0418a', '#6b1082']),
             name="tohoku"),row=1, col=2)

    if 'chubu' in corr_pick:
        chubu = gh[gh['エリア'] == 'chubu']
        l1=chubu['原子力'].iloc[0]
        l2=chubu['火力'].iloc[0]
        l3=chubu['水力'].iloc[0]
        l4=chubu['地熱'].iloc[0]
        l5=chubu['バイオマス'].iloc[0]
        l6=chubu['太陽光'].iloc[0]
        l7=chubu['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7] 
    

        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
             name="chubu"),row=1, col=3)
            
    if 'hokuriku' in corr_pick:
        hokuriku = gh[gh['エリア'] == 'hokuriku']
        l1=hokuriku['原子力'].iloc[0]
        l2=hokuriku['火力'].iloc[0]
        l3=hokuriku['水力'].iloc[0]
        l4=hokuriku['地熱'].iloc[0]
        l5=hokuriku['バイオマス'].iloc[0]
        l6=hokuriku['太陽光'].iloc[0]
        l7=hokuriku['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
            name="hokuriku"),row=1, col=4)

    if 'tokyo' in corr_pick:
        tokyo = gh[gh['エリア'] == 'tokyo']
        l1=tokyo['原子力'].iloc[0]
        l2=tokyo['火力'].iloc[0]
        l3=tokyo['水力'].iloc[0]
        l4=tokyo['地熱'].iloc[0]
        l5=tokyo['バイオマス'].iloc[0]
        l6=tokyo['太陽光'].iloc[0]
        l7=tokyo['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
            name="tokyo"),row=1, col=5)     #どの場所に表示するか

    if 'kansai' in corr_pick:
        kansai = gh[gh['エリア'] == 'kansai']
        l1=kansai['原子力'].iloc[0]
        l2=kansai['火力'].iloc[0]
        l3=kansai['水力'].iloc[0]
        l4=kansai['地熱'].iloc[0]
        l5=kansai['バイオマス'].iloc[0]
        l6=kansai['太陽光'].iloc[0]
        l7=kansai['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7] 

        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
                name="kansai"),row=2, col=1)

    if 'chugoku' in corr_pick:
        chugoku = gh[gh['エリア'] == 'chugoku']
        l1=chugoku['原子力'].iloc[0]
        l2=chugoku['火力'].iloc[0]
        l3=chugoku['水力'].iloc[0]
        l4=chugoku['地熱'].iloc[0]
        l5=chugoku['バイオマス'].iloc[0]
        l6=chugoku['太陽光'].iloc[0]
        l7=chugoku['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7]
    

        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
             name="chugoku"),row=2, col=2)
     
    if 'sikoku' in corr_pick: 
        sikoku = gh[gh['エリア'] == 'sikoku']
        l1=sikoku['原子力'].iloc[0]
        l2=sikoku['火力'].iloc[0]
        l3=sikoku['水力'].iloc[0]
        l4=sikoku['地熱'].iloc[0]
        l5=sikoku['バイオマス'].iloc[0]
        l6=sikoku['太陽光'].iloc[0]
        l7=sikoku['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
            name="sikoku"),row=2, col=3)
    
    if 'kyushu' in corr_pick: 
        kyushu = gh[gh['エリア'] == 'kyushu']
        l1=kyushu['原子力'].iloc[0]
        l2=kyushu['火力'].iloc[0]
        l3=kyushu['水力'].iloc[0]
        l4=kyushu['地熱'].iloc[0]
        l5=kyushu['バイオマス'].iloc[0]
        l6=kyushu['太陽光'].iloc[0]
        l7=kyushu['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
            name="kyushu"),row=2, col=4)
    
    if 'okinawa' in corr_pick: 
        okinawa = gh[gh['エリア'] == 'okinawa']
        l1=okinawa['原子力'].iloc[0]
        l2=okinawa['火力'].iloc[0]
        l3=okinawa['水力'].iloc[0]
        l4=okinawa['地熱'].iloc[0]
        l5=okinawa['バイオマス'].iloc[0]
        l6=okinawa['太陽光'].iloc[0]
        l7=okinawa['風力'].iloc[0]

        pie = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Pie(
                 values=pie,
                 labels=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
            name="okinawa"),row=2, col=5)
    

 
    fig.update_layout(
  #  width=320,
    height=700,
    margin=dict(l=30, r=10, t=100, b=10),
    title = "各社エリアごとの発電電力量割合  "f"日付: {title2}"
    )

    return fig


@ app.callback(Output('kyokyu_marker',  'children'), Input('pg', 'value'),  #ドロップダウン選択で動かす
State('my-cat-picker', 'value'), State('date', 'start_date'))
def kyokyumarkar(#s, n_clicks,
power_gene,value,start_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    drop_down = value
    if drop_down == '1day':
        df = pd.read_csv("csv/1day_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'])
    elif drop_down == '1month':
        df = pd.read_csv("csv/1month_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
    else:
        df = pd.read_csv("csv/time_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATETIME'].astype(str))

    start = start_date
    gh = df[(df['DATETIME'] == start)]  # 表示する日付抽出
    gh['DATETIME'] =pd.Timestamp(start)
    title2 = start
#スライドバーあるならいらない？
   # if selected_id == 'my-button2':
    #    start = start_date
     #   gh = df[(df['DATETIME'] == start)]  # 表示する日付抽出
      #  gh['DATETIME'] =pd.Timestamp(start)
       # title2 = start
    #start = datetime.strptime(start_date[:10], '%Y-%m-%d') 時間もでる

   # if selected_id == 'slider2':
    #    start = pd.to_datetime(markp[s].astype(str))
     #   gh = df[(df['DATETIME'] == start[s[0]])]  # 表示する日付抽出
      #  gh['DATETIME'] =pd.Timestamp(markp[s[0]])
       # title2 = markp[s[0]]

    pg = power_gene
    if pg == '火力':
        gh['火力']=gh['火力'].astype(float)
        gh2 = gh.loc[:,['火力','エリア','DATETIME','lat','lon']]
        fig = px.scatter_geo(
        gh2,
        lat='lat',
        lon='lon',
        color="エリア",
        hover_name=pg,
        size='火力',
        projection='natural earth',
    )

    elif pg == '水力':
        gh['水力']=gh['水力'].astype(float)
        gh2 = gh.loc[:,['水力','エリア','DATETIME','lat','lon']]
        fig = px.scatter_geo(
        gh2,
        lat='lat',
        lon='lon',
        color="エリア",
        hover_name=pg,
        size='水力',
        projection='natural earth',
    )

    elif pg == '太陽光':
        gh['太陽光']=gh['太陽光'].astype(float)
        gh2 = gh.loc[:,['太陽光','エリア','DATETIME','lat','lon']]
        fig = px.scatter_geo(
        gh2,
        lat='lat',
        lon='lon',
        color="エリア",
        hover_name=pg,
        size='太陽光',
        projection='natural earth',
    )

    elif pg == 'バイオマス':
        gh['バイオマス']=gh['バイオマス'].astype(float)
        gh2 = gh.loc[:,['バイオマス','エリア','DATETIME','lat','lon']]
        fig = px.scatter_geo(
        gh2,
        lat='lat',
        lon='lon',
        color="エリア",
        hover_name=pg,
        size='バイオマス',
        projection='natural earth',
    )

    elif pg == '風力':
        gh['風力']=gh['風力'].astype(float)
        gh2 = gh.loc[:,['風力','エリア','DATETIME','lat','lon']]
        fig = px.scatter_geo(
        gh2,
        lat='lat',
        lon='lon',
        color="エリア",
        hover_name=pg,
        size='風力',
        projection='natural earth',
    )

    elif pg == '原子力':
        gh['原子力']=gh['原子力'].astype(float)
        gh2 = gh.loc[:,['原子力','エリア','DATETIME','lat','lon']]
        fig = px.scatter_geo(
        gh2,
        lat='lat',
        lon='lon',
        color="エリア",
        hover_name=pg,
        size='原子力',
        projection='natural earth',
    )

    else:
        gh['地熱']=gh['地熱'].astype(float)
        gh2 = gh.loc[:,['地熱','エリア','DATETIME','lat','lon']]
        fig = px.scatter_geo(
        gh2,
        lat='lat',
        lon='lon',
        color="エリア",
        hover_name=pg,
        size='地熱',
        projection='natural earth',
    )

    fig.update_layout(
        height=600,
        
        title={
            'text': "日本の"f"{pg}発電電力量  "f"日付: {title2}",
            'font':{
                'size':25
            },
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        geo = dict(
            resolution = 50,
            landcolor = 'rgb(204, 204, 204)',
            lataxis = dict(
                range = [28, 47],
            ),
            lonaxis = dict(
                range = [125, 150],
            ),
        )
    )
    return dcc.Graph(
                figure = fig
            )



@ app.callback(Output('bar_chart',  'figure'), 
[Input('slider', 'value'), Input('my-button', 'n_clicks'), ],
State('my-corr-picker', 'value'),State('my-cat-picker', 'value'), State('date', 'start_date'))
def barchart(s, n_clicks,corr_pick,value,start_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    drop_down = value
    if drop_down == '1day':
        df = pd.read_csv("csv/1day_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'])
    elif drop_down == '1month':
        df = pd.read_csv("csv/1month_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
    else:
        df = pd.read_csv("csv/time_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATETIME'].astype(str))

    if selected_id == 'my-button':
        start = start_date
        gh = df[(df['DATETIME'] == start)]  # 表示する日付抽出
        title2 = start
    # start = datetime.strptime(start_date[:10], '%Y-%m-%d') 時間もでる

    if selected_id == 'slider':
        start = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] == start[s[0]])]  # 表示する日付抽出
        title2 = markp[s[0]]
    
    strPC = [str(num) for num in corr_pick]

    #fig = make_subplots(rows=1, cols=5)

#labelの作成が必要　凡例をつくる
    fig = make_subplots(
        rows=2, cols=5,  # 行数と列数
       # vertical_spacing=0.1,  # 表とグラフの間の間隔を0に
        specs=[[{"type": "bar"}, {"type": "bar"},{"type": "bar"},{"type": "bar"},{"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"},{"type": "bar"},{"type": "bar"},{"type": "bar"}]
               ],  # subplotするグラフの配置順やグラフの種類
        subplot_titles=['北海道電力','東北電力','中部電力','北陸電力','東京電力',
                        '関西電力', '中国電力', '四国電力', '九州電力','沖縄電力'],
        )

     
    if 'hokkaido' in corr_pick:
        hokkaido = gh[gh['エリア'] == 'hokkaido']
        l1=hokkaido['原子力'].iloc[0]
        l2=hokkaido['火力'].iloc[0]
        l3=hokkaido['水力'].iloc[0]
        l4=hokkaido['地熱'].iloc[0]
        l5=hokkaido['バイオマス'].iloc[0]
        l6=hokkaido['太陽光'].iloc[0]
        l7=hokkaido['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
            name="hokkaido"),row=1, col=1)
 
    if 'tohoku' in corr_pick:
        tohoku = gh[gh['エリア'] == 'tohoku']
        l1=tohoku['原子力'].iloc[0]
        l2=tohoku['火力'].iloc[0]
        l3=tohoku['水力'].iloc[0]
        l4=tohoku['地熱'].iloc[0]
        l5=tohoku['バイオマス'].iloc[0]
        l6=tohoku['太陽光'].iloc[0]
        l7=tohoku['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7] 

        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
             name="tohoku"),row=1, col=2)

    if 'chubu' in corr_pick:
        chubu = gh[gh['エリア'] == 'chubu']
        l1=chubu['原子力'].iloc[0]
        l2=chubu['火力'].iloc[0]
        l3=chubu['水力'].iloc[0]
        l4=chubu['地熱'].iloc[0]
        l5=chubu['バイオマス'].iloc[0]
        l6=chubu['太陽光'].iloc[0]
        l7=chubu['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7] 
    

        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
             name="chubu"),row=1, col=3)
            
    if 'hokuriku' in corr_pick:
        hokuriku = gh[gh['エリア'] == 'hokuriku']
        l1=hokuriku['原子力'].iloc[0]
        l2=hokuriku['火力'].iloc[0]
        l3=hokuriku['水力'].iloc[0]
        l4=hokuriku['地熱'].iloc[0]
        l5=hokuriku['バイオマス'].iloc[0]
        l6=hokuriku['太陽光'].iloc[0]
        l7=hokuriku['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
            name="hokuriku"),row=1, col=4)

    if 'tokyo' in corr_pick:
        tokyo = gh[gh['エリア'] == 'tokyo']
        l1=tokyo['原子力'].iloc[0]
        l2=tokyo['火力'].iloc[0]
        l3=tokyo['水力'].iloc[0]
        l4=tokyo['地熱'].iloc[0]
        l5=tokyo['バイオマス'].iloc[0]
        l6=tokyo['太陽光'].iloc[0]
        l7=tokyo['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
            name="tokyo"),row=1, col=5)    

    if 'kansai' in corr_pick:
        kansai = gh[gh['エリア'] == 'kansai']
        l1=kansai['原子力'].iloc[0]
        l2=kansai['火力'].iloc[0]
        l3=kansai['水力'].iloc[0]
        l4=kansai['地熱'].iloc[0]
        l5=kansai['バイオマス'].iloc[0]
        l6=kansai['太陽光'].iloc[0]
        l7=kansai['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7] 

        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
                name="kansai"),row=2, col=1)

    if 'chugoku' in corr_pick:
        chugoku = gh[gh['エリア'] == 'chugoku']
        l1=chugoku['原子力'].iloc[0]
        l2=chugoku['火力'].iloc[0]
        l3=chugoku['水力'].iloc[0]
        l4=chugoku['地熱'].iloc[0]
        l5=chugoku['バイオマス'].iloc[0]
        l6=chugoku['太陽光'].iloc[0]
        l7=chugoku['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7]
    

        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
             name="chugoku"),row=2, col=2)
     
    if 'sikoku' in corr_pick: 
        sikoku = gh[gh['エリア'] == 'sikoku']
        l1=sikoku['原子力'].iloc[0]
        l2=sikoku['火力'].iloc[0]
        l3=sikoku['水力'].iloc[0]
        l4=sikoku['地熱'].iloc[0]
        l5=sikoku['バイオマス'].iloc[0]
        l6=sikoku['太陽光'].iloc[0]
        l7=sikoku['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
            name="sikoku"),row=2, col=3)
    
    if 'kyushu' in corr_pick: 
        kyushu = gh[gh['エリア'] == 'kyushu']
        l1=kyushu['原子力'].iloc[0]
        l2=kyushu['火力'].iloc[0]
        l3=kyushu['水力'].iloc[0]
        l4=kyushu['地熱'].iloc[0]
        l5=kyushu['バイオマス'].iloc[0]
        l6=kyushu['太陽光'].iloc[0]
        l7=kyushu['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
            name="kyushu"),row=2, col=4)
    
    if 'okinawa' in corr_pick: 
        okinawa = gh[gh['エリア'] == 'okinawa']
        l1=okinawa['原子力'].iloc[0]
        l2=okinawa['火力'].iloc[0]
        l3=okinawa['水力'].iloc[0]
        l4=okinawa['地熱'].iloc[0]
        l5=okinawa['バイオマス'].iloc[0]
        l6=okinawa['太陽光'].iloc[0]
        l7=okinawa['風力'].iloc[0]

        bar = [l1,l2,l3,l4,l5,l6,l7] 
    
        fig.add_trace(go.Bar(
                 x=['原子力','火力','水力','地熱','バイオマス','太陽光','風力'],
                 y=bar,
            name="okinawa"),row=2, col=5)
    
 
    fig.update_layout(
  #  width=320,
    height=700,
    margin=dict(l=30, r=10, t=100, b=10),
    title = "各社エリアごとの発電電力量  "f"日付: {title2}"
    )

    return fig
  



#raise dash.exceptions.PreventUpdate
if __name__ == '__main__':
    app.run_server(debug=False)

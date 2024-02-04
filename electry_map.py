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


import sqlalchemy as sa
#mysqlの接続
user = 'username'     # ユーザ名
password = 'password' # パスワード
host = 'localhost'    # ホスト名 or IP
db = 'database'       # データベース
port = 3306           # ポート

url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8'

# engine作成
engine = sa.create_engine(url, echo=False)

# pandasのread_sql関数にselect文とengineを指定する
query = "select * from table"
#df = pd.read_sql(query, con=engine)

# 電力データ
df = pd.read_csv("csv/1day_kwh.csv") 
markp = []
markp = df['DATE']
markp_d = {i: markp[i] for i in range(0, 15637, 123)}#DATEの数,スライドバー区切り日付
#統計範囲、期間の設定
drop_down = ['1day', '1month', 'Time']
#発電方法の選択
drop_down2 = ['火力', '水力', '太陽光','バイオマス','風力','原子力','地熱']
#日本の各電力会社
company = [k for k, i in itertools.groupby(df['エリア'])] #####


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
# app = Dash(__name__)

app.title = '電力データマップ'
app.layout = html.Div([
    #タイトル
    html.H2(children='electric power datemap',className='bg-primary'),
    
    dcc.Tabs(id='tabs-example', value='tab-2', children=[
        dcc.Tab([
        html.Div([
            dbc.Row(
                html.H4('電力データマップについて',style={'margin-top': '10px'}
                        ), style={"margin":"0","height": "7vh"}, className='bg-primary text-white font-italic'
            ),
            html.H5(' この電力データマップは日本の電力会社（10社）の電力に関するデータを集め、可視化したものである。近年の電気代値上がりや気候変動による電力逼迫など、日本社会で電力に関する問題が顕著になってきた。この電力危機を脱するために、企業で何ができるだろうか。'),
            html.H5(' 電力のデータに触れ、現状を把握、分析を行い対策を講じていくことが今後必要になると考える。そのためにも、各電力会社の情報をまとめて見ることができるこの電力データマップを役立ててほしい。'),

            html.Div([html.Img(src=app.get_asset_url("colormap.png"),width="700px" ,height="700px",
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
                                    '今回のダッシュボード作成で扱ったデータはでんき予報の使用電力実績を集計したものである。また、それぞれ各社から同じように使用電力を収集し、5年分のデータとして集計を行った。', html.Br(),
                                    '他にも発電方式別にどれくらいの量が発電されているかなど、それぞれの発電所における発電電力量も集計している。', html.Br(),'今後もデータの更新を行っていき、日々新しいデータの統計が行えるようにしていく。'])),

                      html.P(html.Details([html.Summary('使用データの公開'),
                                           'ここでは電力統計で使われている電力データをダウンロードすることが可能である。ただし、元データを加工したものであるため、元データの取得は各電力会社HPより取得してください。', html.Br(),
                                           '　　<CSVファイル>', html.Br(),
                                           '　　　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href="/csv/time_jukyu.csv",download='jukyu_time.csv' ),'　　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='/csv/time_kwh.csv',download='kwh_time.csv' ),html.Br(),
                                           '　　　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href='/Users/mibo/web/csv/1day_jukyu.csv',download='jukyu_day.csv' ),'　　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='/csv/1day_kwh.csv',download='kwh_day.csv' ),html.Br(),
                                           '　　　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href='/csv/1month_jukyu.csv',download='jukyu_month.csv' ),'　　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='/csv/1month_kwh.csv',download='kwh_month.csv' ),html.Br(),

                                           html.Br(),'データの詳しい内容、グラフのカスタムなどは「グラフについて」より行ってください。'])),

                      html.P(html.Details([html.Summary('データの更新状況'),
                                    '2024/2/2現在の更新状況↓', html.Br(),
                                    '2023/10/31までのデータを集計済。'])),

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
    ],label = '概要', value = 'tab-1'),
       
        dcc.Tab([html.Div([
            dbc.Row(
                [
                    html.H4('Settings',
                            style={'margin-top': '10px'})

                ], style={"margin":"0","height": "7vh"}, className='bg-primary text-white font-italic'
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
                                         className='font-weight-bold nav-item dropdown' # className='btn btn-outline-info '
                                         ),
                        ])
                        ] ,style={'width': '30%'}),
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
                        ,style={'width': '30%'}

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
                                         className='font-weight-bold nav-item dropdown'
                                         ),  
                            #実行ボタン、上記３つで決定したものはこのボタンで反映される
                            
                            # className='bg-secondary text-white'

                        ], style={'width': '30%',"height": "25vh"}
                    ),
                    dbc.Row(html.Div([html.H1(
                                html.Button(id='my-button', n_clicks=0, children='apply',
                                            style={'margin-top': '20px',
                                                'right': '15px','align':'center'},
                                            className='btn btn-outline-success btn-lg' ###
                                            ),
                            ),
                        ])
                        ,style={'width': '100%'}
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
                                                max=1600, ##ここで日付の範囲を変更する
                                                # 今回の入力値(初期値)
                                                value=[0, 0],
                                                className='font-weight-bold form-range'), ###
                            ], style={'width': '100%'}
                            ),

                ],style={"width":"100%"})

            ],),

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
                    style={"width":"100%","height": "55vh"}
                ), #矢印マップのとなりはエリア別発電量
                        dbc.Row([
                            dbc.Col(
                            [
                                html.H4('入力した日付期間の比較',style={'margin-top': '30px',
                                          'margin-bottom': '5px', 'left': '10px'},),
                                html.Div(id='title_text',
                                         style={'fontSize': 20}  # フォントサイズを20に設定
                                ),
                                html.Div(id='japan_marker',)#style={'margin-top': '50px', }
                            ],style={"width":"50%",},#"height": "90vh",
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
                        
                        html.Div(dcc.Graph(id='kyokyu_marker',figure={}))
                        
                    ])
                    ],style={"width":"100%"}
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
                style={"width":"100%","height": "90vh",}
                        
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
               style={"width":"100%","height": "100vh",}
                ),
                        ],style={"width":"100%",}
                        )
            # className='bg-dark'
    ],label='電力統計', value='tab-2'),
        
        dcc.Tab([ 
                html.Div([
                    dbc.Row(
            
            html.H4('電力統計のグラフについて',style={'margin-top': '10px'}), style={"margin":"0","height": "7vh"},className='bg-primary text-white font-italic'
                    ), 
            html.Div([html.P(
                html.Details([html.Summary('電力使用量の折れ線グラフ'),
                              '特定の期間内での電力消費のトレンドやパターンを把握することができる。',
                              '', html.Br(),])),

                      html.P(html.Details([html.Summary('電力使用量の増減グラフ'),
                                    '日付期間の選択より、選択した最後の日付から最初の選択日を引いた値が示されている。数値を１つ１つ比較しなくても色と矢印のマークを使うことで、直感的に増減を見ることができる。全国の電力使用量の比較や地域の違いを把握することができる。'])),

                      html.P(html.Details([html.Summary('発電電力量割合の円グラフ'),
                                           '特定の日で各電力会社の発電電力量の割合、発電方式の変化を見ることができる。'])),

                      html.P(html.Details([html.Summary('発電電力量の棒グラフ'),
                                    '円グラフと共に実際の発電電力量を示すことで発電量の具体的な数値を把握することができる。'])),

                      html.P(html.Details([html.Summary('エリアごと発電方式別発電量円グラフ'),
                                    '日本地図にプロットすることで視覚的に発電量を把握できる。'])),

                    html.P(html.Details([html.Summary('電力需給予測のグラフ'),
                                    '発電量と需要量のバランスを視覚化することでピーク時の需要供給の調整や需要制御の重要性を把握できる。'])),

                    html.P(html.Details([html.Summary('詳細なデータのダウンロード'),
                                    '概要のCSVファイルとは別に「Excel」と「CSV」で、各電力会社ごとの電力の発電量、使用量をダウンロードできる。ただし、元データを加工したものであるため、元データの取得は各電力会社HPより取得してください。',html.Br(),
                                    '　【北海道電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href="time_kwh_data/hokkaido.csv",download='hokkaido_jukyu_time.csv',target='_blank' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/hokkaido.csv',download='hokkaido_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/hokkaido_1day_jukyu.csv",download='hokkaido_jukyu_day.csv' ,target='_blank' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/hokkaido.csv',download='hokkaido_kwh_day.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/hokkaidojukyu.csv",download='hokkaido_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='/csv/time_kwh.csv',download='hokkaido_kwh_month.csv' ),html.Br(),
                                           
                                    '　【東北電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_data/tohoku.csv',download='tohoku_jukyu_time.csv' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/tohoku.csv',download='tohoku_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/tohoku.csv",download='tohoku_jukyu_day.csv' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/tohoku.csv',download='tohoku_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/tohoku.csv",download='tohoku_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='day_kwh_data/tohoku.csv',download='tohoku_kwh_time.csv' ),html.Br(),
                                           
                                    '　【東京電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_data/tokyo.csv',download='tokyo_jukyu_time.csv' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/tokyo.csv',download='tokyo_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/tokyo.csv",download='tokyo_jukyu_day.csv' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/tokyo.csv',download='tokyo_kwh_day.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/tokyo.csv",download='tokyo_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='month_kwh_data/tokyo.csv',download='tokyo_kwh_month.csv' ),html.Br(),
                                           
                                    '　【北陸電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_data/hokuriku.csv',download='hokuriku_jukyu_time.csv' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/hokuriku.csv',download='hokuriku_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/hokuriku.csv",download='hokuriku_jukyu_day.csv' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/hokuriku.csv',download='hokuriku_kwh_day.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/hokuriku.csv",download='hokuriku_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='month_kwh_data/hokuriku.csv',download='hokuriku_kwh_month.csv' ),html.Br(),
                                           
                                    '　【中部電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_data/chubu.csv',download='chubu_jukyu_time.csv' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/chubu.csv',download='chubu_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/chubu.csv",download='chubu_jukyu_day.csv' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/chubu.csv',download='chubu_kwh_day.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/chubu.csv",download='chubu_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='month_kwh_data/chubu.csv',download='chubu_kwh_month.csv' ),html.Br(),
                                           
                                    '　【関西電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_data/kansai.csv',download='kansai_jukyu_time.csvv' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/kansai.csv',download='kansai_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/kansai.csv",download='kansai_jukyu_day.csv' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/kansai.csv',download='kansai_kwh_day.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/kansai.csv",download='kansai_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='month_kwh_data/kansai.csv',download='kansai_kwh_month.csv' ),html.Br(),
                                           
                                    '　【中国電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_data/chugoku.csv',download='chugoku_jukyu_time.csv' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/chugoku.csv',download='chugoku_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/chugoku.csv",download='chugoku_jukyu_day.csv' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/chugoku.csv',download='chugoku_kwh_day.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/chugoku.csv",download='chugoku_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='month_kwh_data/chugoku.csv',download='chugoku_kwh_month.csv' ),html.Br(),
                                           
                                    '　【四国電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_data/sikoku.csv',download='sikoku_jukyu_time.csv' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/sikoku.csv',download='sikoku_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/sikoku.csv",download='sikoku_jukyu_day.csv' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/sikoku.csv',download='sikoku_kwh_day.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/sikoku.csv",download='sikoku_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='month_kwh_data/sikoku.csv',download='sikoku_kwh_month.csv' ),html.Br(),
                                           
                                    '　【九州電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_data/kyushu.csv',download='kyushu_jukyu_time.csv' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/kyushu.csv',download='kyushu_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/kyushu.csv",download='kyushu_jukyu_day.csv' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/kyushu.csv',download='kyushu_kwh_day.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/kyushu.csv",download='kyushu_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='month_kwh_data/kyushu.csv',download='kyushu_kwh_month.csv' ),html.Br(),
                                           
                                    '　【沖縄電力】',html.Br(),
                                           '　　　　・',html.A('「電力発電量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_data/okinawa.csv',download='okinawa_jukyu_time.csv' ),'　　　　・',html.A('「電力使用量_1時間ごとの集計」CSVをダウンロード',href='time_kwh_date/okinawa.csv',download='okinawa_kwh_time.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1日ごとの集計」CSVをダウンロード',href="1day_jukyu_data/okinawa.csv",download='okinawa_jukyu_day.csv' ),'　　　　　・',html.A('「電力使用量_1日ごとの集計」CSVをダウンロード',href='day_kwh_data/okinawa.csv',download='okinawa_kwh_day.csv' ),html.Br(),
                                           '　　　　・',html.A('「電力発電量_1月ごとの集計」CSVをダウンロード',href="1time_jukyu_data/okinawa.csv",download='okinawa_jukyu_month.csv' ),'　　　　　・',html.A('「電力使用量_1月ごとの集計」CSVをダウンロード',href='month_kwh_data/okinawa.csv',download='okinawa_kwh_month.csv' ),html.Br(),
                                           

                                          html.Br(),'以下のグラフのカスタムなどで活用してください。※vizGPTはCSVのみアップロード可'

                                    ])),

            html.Div([
                     html.H5('　<chatGPTを使ったグラフのカスタマイズ>'),'　　　',
                     html.A(html.B('[vizGPTでカスタマイズ]'), href='https://vizgpt.ai/workspace', target='_blank'),html.Br(),
                     '　vizGPTとは？',html.Br(),'→vizGPTは、GPTモデルの機能を活用してデータの可視化を作成するツールのことである。自然言語のクエリを解釈し、対応する可視化を生成することで、ユーザーがデータを理解し分析することを容易にする。',html.Br(),
                     '以下は、VizGPTの使用方法を示すクイックビデオデモです：',html.Br(),
                     html.Iframe(src="https://www.youtube.com/embed/a7BW0cYyzwk?list=TLGGaybGDxmkAAkwNDAyMjAyNA", width="832", height="468")
                 #    <iframe width="832" height="468"  title="VizGPT: Make contextual data visualization with Chat Interface" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
            ])

             ])
        ], )#className='bg-dark'
    ], label = 'グラフについて', value = 'tab-3'),
]),html.Div(id='tabs-example-content', ),])



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


@app.callback([Output('japan_marker', 'children'),Output('title_text','children')],
              [Input('slider', 'value'), Input('my-button', 'n_clicks'), ],
              [State('my-cat-picker', 'value'),
               State('date', 'start_date'),State('date', 'end_date')])
def japanmarker(s, n_clicks, value,start_date, end_date):
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

    if selected_id == 'slider':
        date = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] >= date[s[0]])
              #      &(df['DATETIME'] <= date[s[1]])
                    ]  # 表示する日付抽出
        start = markp[s[0]]
        end = markp[s[1]]

    #ボタンでセッティングを変更したときの処理
    if selected_id == 'my-button':
        start = start_date
        end = end_date
        gh = df[(df['DATETIME'] >= start)
            #     & (df['DATETIME'] <= end)
            ]
        
    text_output = f'日付期間:{end}から {start}を引いた電力使用量の差'
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
    s5 = dfs5['合計'].iloc[0] # 最初の合計値
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

    # 北海道電力
    dfs6 = gh[gh['エリア'] == 'hokkaido']
    s6 = dfs6['合計'].iloc[0]  # 最初の合計値
    e6 = dfs6['合計'].iloc[-1]  # 最後の合計値
    if s6 > e6:
        comp_down = s6 - e6
        popup = folium.Popup(f"{comp_down}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      43.06172661, 141.3576819], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e6 - s6
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      43.06172661, 141.3576819], icon=icon, popup=popup).add_to(map)
    # 北陸電力
    dfs7 = gh[gh['エリア'] == 'hokuriku']
    s7 = dfs7['合計'].iloc[0]  # 最初の合計値
    e7 = dfs7['合計'].iloc[-1]  # 最後の合計値
    if s7 > e7:
        comp_down = s7 - e7
        popup = folium.Popup(f"{comp_down}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      36.70291844,137.2150143], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e7 - s7
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      36.70291844,137.2150143], icon=icon, popup=popup).add_to(map)
    # 九州電力
    dfs8 = gh[gh['エリア'] == 'kyushu']
    s8 = dfs8['合計'].iloc[0]  # 最初の合計値
    e8 = dfs8['合計'].iloc[-1]  # 最後の合計値
    if s8 > e8:
        comp_down = s8 - e8
        popup = folium.Popup(f"{comp_down}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      33.58376482,130.4045583], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e8 - s8
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      33.58376482,130.4045583], icon=icon, popup=popup).add_to(map)
        
    # 沖縄電力
    dfs9 = gh[gh['エリア'] == 'okinawa']
    s9 = dfs9['合計'].iloc[0]  # 最初の合計値
    e9 = dfs9['合計'].iloc[-1]  # 最後の合計値
    if s9 > e9:
        comp_down = s9 - e9
        popup = folium.Popup(f"{comp_down}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      26.26974929,127.7161896], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e9 - s9
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      26.26974929,127.7161896], icon=icon, popup=popup).add_to(map)
        
    # 四国電力
    dfs10 = gh[gh['エリア'] == 'sikoku']
    s10 = dfs10['合計'].iloc[0]  # 最初の合計値
    e10 = dfs10['合計'].iloc[-1]  # 最後の合計値
    if s10 > e10:
        comp_down = s10 - e10
        popup = folium.Popup(f"{comp_down}万kw減少", max_width=300)
        icon = CustomIcon(
            icon_image="images/down.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      34.34794313,134.0501999], icon=icon, popup=popup).add_to(map)
    else:
        comp_up = e10 - s10
        popup = folium.Popup(f"{comp_up}万kw増加", max_width=300)
        icon = CustomIcon(
            icon_image="images/up.png", icon_size=(55, 65), icon_anchor=(30, 30),
            popup_anchor=(3, 3))
        folium.Marker(location=[
                      34.34794313,134.0501999], icon=icon, popup=popup).add_to(map)


    map.save('compmap.html')
    new = 'compmap.html'
    #text_output = f'日付期間{end}から  {start}の比較'
    iframe_src = html.Iframe(srcDoc=open(new, 'r').read(), width='100%', height='550')
    return   iframe_src,text_output


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
        gh = df[(df['DATETIME'] >= start)]  # 表示する日付抽出
        if drop_down == '1month':
            title2 = start[6] + '月のデータ'
        else:
            title2 = start
    # start = datetime.strptime(start_date[:10], '%Y-%m-%d') 時間もでる

    if selected_id == 'slider':
        date = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] >= date[s[0]])]  # 表示する日付抽出
        if drop_down == '1month':
            title2 = markp[s[0]][5] + '月のデータ'
        else:
            title2 = markp[s[0]]
    
    strPC = [str(num) for num in corr_pick]

    

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
                 name="hokkaido",
                 marker=dict(colors=['#bad6eb', '#2b7bba']),
                 ),row=1, col=1)
 
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
                 name="okinawa"
                 ),row=2, col=5)
    

 
    fig.update_layout(
  #  width=320,
    height=700,
    margin=dict(l=30, r=10, t=100, b=10),
    title = "各社エリアごとの発電電力量割合  "f" {title2}"
    )

    return fig


@ app.callback(Output('kyokyu_marker',  'figure'),
               [Input('slider', 'value'), Input('my-button', 'n_clicks'), Input('pg', 'value'),],  #ドロップダウン選択で動かす
State('my-cat-picker', 'value'), State('date', 'start_date'))
def kyokyumarkar(s, n_clicks,
power_gene,value,start_date):
    selected_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    
    drop_down = value
    if drop_down == '1day':
        df = pd.read_csv("csv/1day_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE']) 
        start = start_date
    elif drop_down == '1month':
        df = pd.read_csv("csv/1month_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
        #タイムスタンプに変換
        start_date_t = pd.Timestamp(start_date)
        #年月を取り出し、日付は1日に指定
        start_year = start_date_t.year
        start_month = start_date_t.month
        start_day = 1  
        start = pd.Timestamp(year=start_year, month=start_month, day=start_day)#抽出する日時を再作成
    else:
        df = pd.read_csv("csv/time_jukyu.csv")
        df['DATETIME'] = pd.to_datetime(df['DATETIME'].astype(str))
        start = start_date

    if selected_id == 'slider':
        if drop_down == '1month':
            date = pd.to_datetime(markp[s].astype(str))
            d = date[s[0]]
            date_t = pd.Timestamp(d)
            date_year = date_t.year
            date_month = date_t.month
            date_day = 1
            date1 =pd.Timestamp(year=date_year,month=date_month,day=date_day)
            gh = df[(df['DATETIME'] == date1)]  
            title2 =   markp[s[0]]
        else:# 1month以外の場合の処理
            date = pd.to_datetime(markp[s].astype(str))
            gh = df[(df['DATETIME'] == date[s[0]])]  # 表示する日付抽出
            title2 = markp[s[0]]
            
    if selected_id == 'my-button' :
        gh = df[(df['DATETIME'] == start)]  # 表示する日付抽出
        title2 = start_date
    if selected_id == 'pg': #基本はスライダーから日付取得、ボタンを押した時はその時点で選択していた発電方式を表示
        gh = df[(df['DATETIME'] == start)]  
        title2 = start_date
        if 0 in markp:
            date = pd.to_datetime(markp[s].astype(str))
            gh = df[(df['DATETIME'] == date[s[0]])]  # 表示する日付抽出
            title2 = markp[s[0]]


    #    date = pd.to_datetime(markp[s].astype(str))
     #   gh = df[(df['DATETIME'] == date[s[0]])]  
      #  title2 = markp[s[0]]
        
    pg = power_gene
    if pg == '火力':
        gh.loc[:, '火力']=gh['火力'].astype(float)
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
        gh.loc[:, '水力']=gh['水力'].astype(float)
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
        gh.loc[:, '太陽光']=gh['太陽光'].astype(float)
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
        gh.loc[:, 'バイオマス']=gh['バイオマス'].astype(float)
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
        gh.loc[:, '風力']=gh['風力'].astype(float)
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
        gh.loc[:, '原子力']=gh['原子力'].astype(float)
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
        gh.loc[:, '地熱']=gh['地熱'].astype(float)
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
    return fig
            



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
        gh = df[(df['DATETIME'] >= start)]  # 表示する日付抽出
        if drop_down == '1month':
            title2 =start[6] + '月のデータ'
        else:
            title2 = start
    # start = datetime.strptime(start_date[:10], '%Y-%m-%d') 時間もでる

    if selected_id == 'slider':
        start = pd.to_datetime(markp[s].astype(str))
        gh = df[(df['DATETIME'] >= start[s[0]])]  # 表示する日付抽出
        if drop_down == '1month':
            title2 = markp[s[0]][5] + '月のデータ'
        else:
            title2 = markp[s[0]]

    strPC = [str(num) for num in corr_pick]


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
    label = {'太陽光':'#00CC96',
        '風力':'#636EFA'}

    bar = [{'x':'原子力','c':'#bad6eb'},
               {'x':'火力','c':'#2b7bba'},
               {'x':'水力','c':'#EF553B'},
               {'x':'地熱','c':'#FFA15A'},
               {'x':'バイオマス','c':'#AB63FA'},
               {'x':'太陽光','c':'#00CC96'},
               {'x':'風力','c':'#636EFA'},]
    df_bar = pd.DataFrame(data=bar)


    if 'hokkaido' in corr_pick:
        hokkaido = gh[gh['エリア'] == 'hokkaido']
        l1=hokkaido['原子力'].iloc[0]
        l2=hokkaido['火力'].iloc[0]
        l3=hokkaido['水力'].iloc[0]
        l4=hokkaido['地熱'].iloc[0]
        l5=hokkaido['バイオマス'].iloc[0]
        l6=hokkaido['太陽光'].iloc[0]
        l7=hokkaido['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                      row=1, col=1)

    if 'tohoku' in corr_pick:
        tohoku = gh[gh['エリア'] == 'tohoku']
        l1=tohoku['原子力'].iloc[0]
        l2=tohoku['火力'].iloc[0]
        l3=tohoku['水力'].iloc[0]
        l4=tohoku['地熱'].iloc[0]
        l5=tohoku['バイオマス'].iloc[0]
        l6=tohoku['太陽光'].iloc[0]
        l7=tohoku['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                          row=1, col=2)

    if 'chubu' in corr_pick:
        chubu = gh[gh['エリア'] == 'chubu']
        l1=chubu['原子力'].iloc[0]
        l2=chubu['火力'].iloc[0]
        l3=chubu['水力'].iloc[0]
        l4=chubu['地熱'].iloc[0]
        l5=chubu['バイオマス'].iloc[0]
        l6=chubu['太陽光'].iloc[0]
        l7=chubu['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                      row=1, col=3)

    if 'hokuriku' in corr_pick:
        hokuriku = gh[gh['エリア'] == 'hokuriku']
        l1=hokuriku['原子力'].iloc[0]
        l2=hokuriku['火力'].iloc[0]
        l3=hokuriku['水力'].iloc[0]
        l4=hokuriku['地熱'].iloc[0]
        l5=hokuriku['バイオマス'].iloc[0]
        l6=hokuriku['太陽光'].iloc[0]
        l7=hokuriku['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                      row=1, col=4)

    if 'tokyo' in corr_pick:
        tokyo = gh[gh['エリア'] == 'tokyo']
        l1=tokyo['原子力'].iloc[0]
        l2=tokyo['火力'].iloc[0]
        l3=tokyo['水力'].iloc[0]
        l4=tokyo['地熱'].iloc[0]
        l5=tokyo['バイオマス'].iloc[0]
        l6=tokyo['太陽光'].iloc[0]
        l7=tokyo['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                          row=1, col=5)

    if 'kansai' in corr_pick:
        kansai = gh[gh['エリア'] == 'kansai']
        l1=kansai['原子力'].iloc[0]
        l2=kansai['火力'].iloc[0]
        l3=kansai['水力'].iloc[0]
        l4=kansai['地熱'].iloc[0]
        l5=kansai['バイオマス'].iloc[0]
        l6=kansai['太陽光'].iloc[0]
        l7=kansai['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                          row=2, col=1)

    if 'chugoku' in corr_pick:
        chugoku = gh[gh['エリア'] == 'chugoku']
        l1=chugoku['原子力'].iloc[0]
        l2=chugoku['火力'].iloc[0]
        l3=chugoku['水力'].iloc[0]
        l4=chugoku['地熱'].iloc[0]
        l5=chugoku['バイオマス'].iloc[0]
        l6=chugoku['太陽光'].iloc[0]
        l7=chugoku['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                      row=2, col=2)
     
    if 'sikoku' in corr_pick: 
        sikoku = gh[gh['エリア'] == 'sikoku']
        l1=sikoku['原子力'].iloc[0]
        l2=sikoku['火力'].iloc[0]
        l3=sikoku['水力'].iloc[0]
        l4=sikoku['地熱'].iloc[0]
        l5=sikoku['バイオマス'].iloc[0]
        l6=sikoku['太陽光'].iloc[0]
        l7=sikoku['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                          row=2, col=3)

    if 'kyushu' in corr_pick: 
        kyushu = gh[gh['エリア'] == 'kyushu']
        l1=kyushu['原子力'].iloc[0]
        l2=kyushu['火力'].iloc[0]
        l3=kyushu['水力'].iloc[0]
        l4=kyushu['地熱'].iloc[0]
        l5=kyushu['バイオマス'].iloc[0]
        l6=kyushu['太陽光'].iloc[0]
        l7=kyushu['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                          row=2, col=4)
    
    if 'okinawa' in corr_pick: 
        okinawa = gh[gh['エリア'] == 'okinawa']
        l1=okinawa['原子力'].iloc[0]
        l2=okinawa['火力'].iloc[0]
        l3=okinawa['水力'].iloc[0]
        l4=okinawa['地熱'].iloc[0]
        l5=okinawa['バイオマス'].iloc[0]
        l6=okinawa['太陽光'].iloc[0]
        l7=okinawa['風力'].iloc[0]

        df_bar['y'] = [l1,l2,l3,l4,l5,l6,l7]
        
        fig.add_trace(go.Bar(x=df_bar['x'],y=df_bar['y'],marker_color=df_bar['c']),#,name='x'
                          row=2, col=5)
        
    
    fig.update_layout(
        showlegend=False,
  #  width=320,
    height=900,
    margin=dict(l=30, r=100, t=100, b=10),
    title = "各社エリアごとの発電電力量  "f"日付: {title2}"
    )

    return fig
  



#raise dash.exceptions.PreventUpdate
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)

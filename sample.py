import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

app = Dash(__name__)

df = pd.read_csv("fruit.csv")

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Dash動作確認、棒グラフ'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Tabs(
        value="one",  # 初期選択タブ
        children=[
            dcc.Tab(label='タブ１', value="one",
                    children=html.H3('タブ１の内容')
                    ),
            dcc.Tab(label='タブ２', value="two",
                    children=html.H3('タブ２の内容'))
        ]
    )
])
html.Div(children=[
    html.H1(children='Dash動作確認、棒グラフ'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
[dcc.Graph(
    id='example-graph',
    figure=fig
)]

app.layout = html.Div([
    html.H4(children='default of credit card clients Data Set'),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='raw data', value='tab-1'),
        dcc.Tab(label='number of missing values', value='tab-2'),
        dcc.Tab(label='stats', value='tab-3')

    ]),
    html.Div(id='tabs-example-content'),

])


@app.callback(Output('tabs-example-content', 'children'), Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            children=
        html.H1(children='Dash動作確認、棒グラフ'

        ])
        elif tab == 'tab-2':
        return html.Div([
            children=
        html.H1(children='Dash動作確認、棒グラフ'

        ])
        elif tab == 'tab-3':
        return html.Div([
            children=
        html.H1(children='Dash動作確認、棒グラフ'

        ])

        if __name__ == '__main__':
            app.run_server(debug=True)

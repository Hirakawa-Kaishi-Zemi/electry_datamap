from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
 
app = Dash(__name__)
 
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("fruit.csv")
 
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
 
app.layout = html.Div(children=[
    html.H1(children='Dash動作確認、棒グラフ'),
 
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
 
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
 
if __name__ == '__main__':
    app.run_server(debug=True)
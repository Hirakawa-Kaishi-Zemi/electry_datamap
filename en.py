# ライブラリをインポート
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
# サンプルデータセットを読み込む

df = pd.read_csv("csv/1day_jukyu.csv")
df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
gh = df[(df['DATETIME'] == '2019/4/1')]

#tokyoの円グラフ
tokyo = gh[gh['エリア'] == 'tokyo']

l0=tokyo['合計'].iloc[0]
l1=tokyo['原子力'].iloc[0]
l2=tokyo['火力'].iloc[0]
l3=tokyo['水力'].iloc[0]
l4=tokyo['地熱'].iloc[0]
l5=tokyo['バイオマス'].iloc[0]
l6=tokyo['太陽光発電実績'].iloc[0]
l7=tokyo['風力発電実績'].iloc[0]

pie = [l1,l2,l3,l4,l5,l6,l7] 

fig_pie = go.Figure(
    data=[go.Pie(
                 values=pie,
               #  hole=.3,
                 marker=dict(colors=['#bad6eb', '#2b7bba']))])
fig_pie.update_layout(
    width=320,
    height=250,
    margin=dict(l=30, r=10, t=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
)


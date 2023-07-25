# 折れ線グラフプロット
def lineplot_kwh(gh, x_label='DATETIME', y_label='実績(万kW)', label=''):
    x = gh[x_label]
    y = gh[y_label]

    area = gh['エリア'].unique()

    # PLOT
    plt.plot(x, y, marker='o', label=area[0])


# チェックボックス判定
def checkbox():
    PC = [tokyo, kansai, chubu, tohoku, chugoku]
    strPC = [str(num) for num in PC]

    if tokyo == True:
        gh2 = gh[gh['エリア'] == 'tokyo']
        lineplot_kwh(gh2)

    if kansai == True:
        gh2 = gh[gh['エリア'] == 'kansai']
        lineplot_kwh(gh2)

    if chubu == True:
        gh2 = gh[gh['エリア'] == 'chubu']
        lineplot_kwh(gh2)

    if tohoku == True:
        gh2 = gh[gh['エリア'] == 'tohoku']
        lineplot_kwh(gh2)

    if chugoku == True:
        gh2 = gh[gh['エリア'] == 'chugoku']
        lineplot_kwh(gh2)


# 1日集計の折れ線グラフ

# 日付入力
date_from = '2021-01-01'  # @param {type:"date"}
date_to = '2021-02-01'  # @param {type:"date"}

# 電力会社選択
tokyo = True  # @param {type:"boolean"}
kansai = True  # @param {type:"boolean"}
chubu = True  # @param {type:"boolean"}
tohoku = True  # @param {type:"boolean"}
chugoku = False  # @param {type:"boolean"}

import matplotlib.pyplot as plt
# 折れ線グラフ 期間
import pandas as pd

# 電力データ
df = pd.read_csv("csv/1day_kwh.csv")

# datetime型
df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
# gh = df1[(df1['DATETIME'] > datetime(2020,1,31)) & (df1['DATETIME'] < datetime(2020, 2, 29))]


gh = df[(df['DATETIME'] >= date_from) & (df['DATETIME'] <= date_to)]  # 表示する期間のみ抽出

# 電力会社の選択判定
checkbox()

graph_title = f"期間: {date_from} - {date_to}"
plt.title(graph_title)
plt.xlabel("日付")
plt.ylabel("万kw")
plt.legend()
plt.rcParams["figure.figsize"] = (12, 5)

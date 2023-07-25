date_day = '2022-02-09' #@param {type:"date"}


import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from japanmap import picture
import japanize_matplotlib

#電力データ
df = pd.read_csv("csv/1day_kwh.csv")
df1 = pd.read_csv("csv/areamap.csv")


df['DATETIME'] = pd.to_datetime(df['DATE'].astype(str))
gh = df[(df['DATETIME'] == date_day)]  #表示する日付抽出
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

